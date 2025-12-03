// @ts-nocheck

import React from 'react';
import * as apiAuthModule from '@shared/hooks/useApiAuth';
import { act, renderHook, waitFor } from '@testing-library/react';
import { clearAllData } from '../../storage/database';
import { GuestProfileManager } from '../../storage/guestProfile';
import { OutboxManager } from '../../storage/outbox';
import { GuestModeProvider, useGuestMode } from '../useGuestMode';

// Only mock auth; use real storage and managers
jest.mock('@shared/hooks/useApiAuth');

const mockUseApiAuth = apiAuthModule as jest.Mocked<typeof apiAuthModule>;

describe('useGuestMode (integration)', () => {
  let wrapper: React.ComponentType<{ children: React.ReactNode }>;

  beforeEach(async () => {
    await clearAllData();
    jest.clearAllMocks();
    wrapper = ({ children }) => <GuestModeProvider>{children}</GuestModeProvider>;
    // Default unauthenticated
    mockUseApiAuth.useApiAuth.mockReturnValue({ user: null, isLoading: false });
  });

  afterEach(async () => {
    await clearAllData();
  });

  describe('initialization', () => {
    it('initializes guest profile when unauthenticated', async () => {
      const { result } = renderHook(() => useGuestMode(), { wrapper });

      expect(result.current.isLoading).toBe(true);

      await waitFor(() => expect(result.current.isLoading).toBe(false));
      expect(result.current.isGuestMode).toBe(true);
      expect(result.current.guestProfile).not.toBeNull();
    });

    it('does not enter guest mode when authenticated', async () => {
      mockUseApiAuth.useApiAuth.mockReturnValue({
        user: { profile: { sub: 'user-123' } },
        isLoading: false,
      });
      const { result } = renderHook(() => useGuestMode(), { wrapper });
      await waitFor(() => expect(result.current.isLoading).toBe(false));
      expect(result.current.isGuestMode).toBe(false);
      expect(result.current.guestProfile).toBeNull();
    });

    it('respects auth loading state', () => {
      mockUseApiAuth.useApiAuth.mockReturnValue({ user: null, isLoading: true });
      const { result } = renderHook(() => useGuestMode(), { wrapper });
      expect(result.current.isLoading).toBe(true);
    });
  });

  describe('switchToGuestMode', () => {
    it('does nothing when authenticated', async () => {
      mockUseApiAuth.useApiAuth.mockReturnValue({
        user: { profile: { sub: 'auth' } },
        isLoading: false,
      });
      const warn = jest.spyOn(console, 'warn').mockImplementation(() => {});
      const { result } = renderHook(() => useGuestMode(), { wrapper });

      await act(async () => {
        await result.current.switchToGuestMode();
      });
      expect(warn).toHaveBeenCalled();
      warn.mockRestore();
    });
  });

  describe('upgradeToAuthenticatedMode', () => {
    it('migrates guest events and clears guest profile state', async () => {
      // Start in guest mode
      const { result } = renderHook(() => useGuestMode(), { wrapper });
      await waitFor(() => expect(result.current.isGuestMode).toBe(true));
      const guestId = result.current.guestProfile!.guestId;

      // Add some guest events
      await OutboxManager.addEvent(
        'guest-labour-1',
        'start_contraction',
        { start_time: 'x' },
        true
      );
      await OutboxManager.addEvent('guest-labour-1', 'end_contraction', { end_time: 'y' }, true);

      // Become authenticated
      mockUseApiAuth.useApiAuth.mockReturnValue({
        user: { profile: { sub: 'user-123' } },
        isLoading: false,
      });

      await act(async () => {
        await result.current.upgradeToAuthenticatedMode();
      });

      // Profile cleared
      expect(result.current.guestProfile).toBeNull();
      expect(result.current.isGuestMode).toBe(false);

      // Events marked as upgraded (isGuestEvent === 0) and still pending/synced
      const pending = await OutboxManager.getEventsByStatus('pending');
      expect(pending.every((e) => e.isGuestEvent === 0)).toBe(true);

      // Original profile marked upgraded
      const profiles = await GuestProfileManager.getAllGuestProfiles();
      const upgraded = profiles.find((p) => p.guestId === guestId);
      expect(upgraded?.isUpgraded).toBe(1);
    });
  });

  describe('clearGuestData', () => {
    it('removes guest profile and guest events', async () => {
      const { result } = renderHook(() => useGuestMode(), { wrapper });
      await waitFor(() => expect(result.current.isGuestMode).toBe(true));

      // Seed a guest event
      await OutboxManager.addEvent('guest-labour-1', 'start_contraction', {}, true);

      await act(async () => {
        await result.current.clearGuestData();
      });
      expect(result.current.guestProfile).toBeNull();
      expect(result.current.isGuestMode).toBe(false);

      const remainingGuestEvents = await OutboxManager.getGuestEvents();
      expect(remainingGuestEvents.length).toBe(0);

      const profiles = await GuestProfileManager.getAllGuestProfiles();
      expect(profiles.length).toBe(0);
    });
  });

  describe('exportGuestData', () => {
    it('exports guest profile data', async () => {
      const { result } = renderHook(() => useGuestMode(), { wrapper });
      await waitFor(() => expect(result.current.isGuestMode).toBe(true));

      const exportData = await result.current.exportGuestData();
      expect(exportData).toHaveProperty('guestId', result.current.guestProfile!.guestId);
      expect(exportData).toHaveProperty('createdAt');
      expect(Array.isArray(exportData.labours)).toBe(true);
    });

    it('throws when no guest profile', async () => {
      mockUseApiAuth.useApiAuth.mockReturnValue({
        user: { profile: { sub: 'auth' } },
        isLoading: false,
      });
      const { result } = renderHook(() => useGuestMode(), { wrapper });
      await expect(result.current.exportGuestData()).rejects.toThrow('No guest profile to export');
    });
  });

  describe('state transitions', () => {
    it('transitions from guest to authenticated on login', async () => {
      const { result, rerender } = renderHook(() => useGuestMode(), { wrapper });
      await waitFor(() => expect(result.current.isGuestMode).toBe(true));

      mockUseApiAuth.useApiAuth.mockReturnValue({
        user: { profile: { sub: 'auth' } },
        isLoading: false,
      });
      rerender();

      await waitFor(() => {
        expect(result.current.isGuestMode).toBe(false);
        expect(result.current.guestProfile).toBeNull();
      });
    });
  });

  describe('error handling', () => {
    it('throws when used outside provider', () => {
      expect(() => renderHook(() => useGuestMode())).toThrow(
        'useGuestMode must be used within GuestModeProvider'
      );
    });
  });
});
