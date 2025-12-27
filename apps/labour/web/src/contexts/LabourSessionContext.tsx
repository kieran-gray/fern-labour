import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { SubscriberStatus, SubscriptionStatusReadModel } from '@base/clients/labour_service/types';
import { useApiAuth } from '@base/hooks/useApiAuth';

export enum AppMode {
  Subscriber = 'Subscriber',
  Birth = 'Birth',
}

export enum SubscriberSessionState {
  NoSelection = 'no-selection',
  PendingApproval = 'pending-approval',
  Active = 'active',
}

export interface LabourSessionState {
  labourId: string | null;
  subscription: SubscriptionStatusReadModel | null;
  mode: AppMode | null;
}

interface LabourSessionContextType extends LabourSessionState {
  canViewLabour: boolean;
  subscriberState: SubscriberSessionState;

  setLabourId: (labourId: string | null) => void;
  setMode: (mode: AppMode | null) => void;
  selectSubscription: (subscription: SubscriptionStatusReadModel) => void;
  updateSubscription: (subscription: SubscriptionStatusReadModel) => void;
  clearSubscription: () => void;
  clearSession: () => void;
}

const LabourSessionContext = createContext<LabourSessionContextType | undefined>(undefined);

export const LabourSessionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useApiAuth();
  const userId = user?.sub;

  const [mode, setModeState] = useState<AppMode | null>(() => {
    const stored = localStorage.getItem(`${userId}:appMode`);
    return stored === AppMode.Birth || stored === AppMode.Subscriber ? stored : null;
  });

  const [labourId, setLabourIdState] = useState<string | null>(() => {
    return localStorage.getItem(`${userId}:labourId`) || null;
  });

  const [subscription, setSubscriptionState] = useState<SubscriptionStatusReadModel | null>(() => {
    const stored = localStorage.getItem(`${userId}:subscription`);
    if (stored) {
      try {
        return JSON.parse(stored);
      } catch {
        return null;
      }
    }
    return null;
  });

  useEffect(() => {
    if (userId) {
      localStorage.setItem(`${userId}:appMode`, mode || '');
    }
  }, [mode, userId]);

  useEffect(() => {
    if (userId) {
      localStorage.setItem(`${userId}:labourId`, labourId || '');
    }
  }, [labourId, userId]);

  useEffect(() => {
    if (userId) {
      localStorage.setItem(
        `${userId}:subscription`,
        subscription ? JSON.stringify(subscription) : ''
      );
    }
  }, [subscription, userId]);

  const subscriberState = useMemo((): SubscriberSessionState => {
    if (!subscription) {
      return SubscriberSessionState.NoSelection;
    }
    if (subscription.status === SubscriberStatus.SUBSCRIBED) {
      return SubscriberSessionState.Active;
    }
    if (subscription.status === SubscriberStatus.REQUESTED) {
      return SubscriberSessionState.PendingApproval;
    }
    // UNSUBSCRIBED, REMOVED, BLOCKED - treat as no selection
    return SubscriberSessionState.NoSelection;
  }, [subscription]);

  const canViewLabour = useMemo((): boolean => {
    if (mode === AppMode.Birth) {
      return labourId !== null;
    }
    if (mode === AppMode.Subscriber) {
      return subscriberState === SubscriberSessionState.Active;
    }
    return false;
  }, [mode, labourId, subscriberState]);

  const setLabourId = useCallback((id: string | null) => {
    setLabourIdState(id);
  }, []);

  const setMode = useCallback((newMode: AppMode | null) => {
    setModeState(newMode);
    if (newMode === AppMode.Birth) {
      setSubscriptionState(null);
    } else if (newMode === AppMode.Subscriber) {
      setLabourIdState(null);
    }
  }, []);

  const selectSubscription = useCallback((sub: SubscriptionStatusReadModel) => {
    setSubscriptionState(sub);
    setLabourIdState(sub.labour_id);
  }, []);

  const updateSubscription = useCallback((sub: SubscriptionStatusReadModel) => {
    setSubscriptionState(sub);
  }, []);

  const clearSubscription = useCallback(() => {
    setSubscriptionState(null);
    setLabourIdState(null);
  }, []);

  const clearSession = useCallback(() => {
    setLabourIdState(null);
    setSubscriptionState(null);
    setModeState(null);
  }, []);

  const value: LabourSessionContextType = {
    labourId,
    subscription,
    mode,
    canViewLabour,
    subscriberState,
    setLabourId,
    setMode,
    selectSubscription,
    updateSubscription,
    clearSubscription,
    clearSession,
  };

  return <LabourSessionContext.Provider value={value}>{children}</LabourSessionContext.Provider>;
};

export const useLabourSession = () => {
  const context = useContext(LabourSessionContext);
  if (context === undefined) {
    throw new Error('useLabourSession must be used within a LabourSessionProvider');
  }
  return context;
};
