import { createContext, useContext, useEffect, useState } from 'react';
import { useApiAuth } from '@shared/hooks/useApiAuth';
import { GuestProfile } from '../storage/database';
import { GuestProfileManager } from '../storage/guestProfile';
import { OutboxManager } from '../storage/outbox';

interface GuestModeContextType {
  isGuestMode: boolean;
  guestProfile: GuestProfile | null;
  isLoading: boolean;
  switchToGuestMode: () => Promise<void>;
  upgradeToAuthenticatedMode: () => Promise<void>;
  clearGuestData: () => Promise<void>;
  exportGuestData: () => Promise<any>;
}

const GuestModeContext = createContext<GuestModeContextType | null>(null);

/**
 * Provider for guest mode functionality
 */
export function GuestModeProvider({ children }: { children: React.ReactNode }) {
  const { user, isLoading: authLoading } = useApiAuth();
  const [guestProfile, setGuestProfile] = useState<GuestProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const isGuestMode = !user && !authLoading && !!guestProfile;

  useEffect(() => {
    async function initializeGuestMode() {
      if (authLoading) {
        return;
      }

      if (user) {
        setGuestProfile(null);
        setIsLoading(false);
        return;
      }

      try {
        const profile = await GuestProfileManager.getCurrentGuestProfile();
        setGuestProfile(profile);
      } finally {
        setIsLoading(false);
      }
    }

    initializeGuestMode();
  }, [user, authLoading]);

  const switchToGuestMode = async (): Promise<void> => {
    if (user) {
      console.warn('Cannot switch to guest mode while authenticated');
      return;
    }

    setIsLoading(true);
    try {
      const profile = await GuestProfileManager.createGuestProfile();
      setGuestProfile(profile);
    } finally {
      setIsLoading(false);
    }
  };

  const upgradeToAuthenticatedMode = async (): Promise<void> => {
    if (!isGuestMode || !guestProfile) {
      console.warn('Not in guest mode, cannot upgrade');
      return;
    }

    setIsLoading(true);
    try {
      const guestEvents = await OutboxManager.getGuestEvents();

      if (guestEvents.length > 0) {
        const eventIds = guestEvents.map((e) => e.id);
        await OutboxManager.markGuestEventsUpgraded(eventIds);

        // TODO: Trigger sync to send events to server
        // Note: This assumes the sync engine is running and user is now authenticated
      }

      await GuestProfileManager.markAsUpgraded(guestProfile.guestId);

      setGuestProfile(null);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Clear all guest data (user requested deletion)
   */
  const clearGuestData = async (): Promise<void> => {
    if (!guestProfile) {
      return;
    }

    setIsLoading(true);
    try {
      await GuestProfileManager.clearGuestData(guestProfile.guestId);

      const guestEvents = await OutboxManager.getGuestEvents();
      const eventIds = guestEvents.map((e) => e.id);
      await Promise.all(eventIds.map((id) => OutboxManager.deleteEvent(id)));

      setGuestProfile(null);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Export guest data for download/backup
   */
  const exportGuestData = async () => {
    if (!guestProfile) {
      throw new Error('No guest profile to export');
    }
    return await GuestProfileManager.exportGuestData(guestProfile.guestId);
  };

  const contextValue: GuestModeContextType = {
    isGuestMode,
    guestProfile,
    isLoading,
    switchToGuestMode,
    upgradeToAuthenticatedMode,
    clearGuestData,
    exportGuestData,
  };

  return <GuestModeContext.Provider value={contextValue}>{children}</GuestModeContext.Provider>;
}

/**
 * Hook to access guest mode functionality
 */
export function useGuestMode(): GuestModeContextType {
  const context = useContext(GuestModeContext);

  if (!context) {
    throw new Error('useGuestMode must be used within GuestModeProvider');
  }

  return context;
}

/**
 * Simple hook to check if currently in guest mode
 */
export function useIsGuestMode(): boolean {
  const { isGuestMode } = useGuestMode();
  return isGuestMode;
}
