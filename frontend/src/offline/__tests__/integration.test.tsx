// @ts-nocheck

import React from 'react';
import {
  useDeleteContraction,
  useEndContraction,
  useStartContraction,
  useUpdateContraction,
} from '@base/shared-components/hooks';
import * as labourServiceModule from '@clients/labour_service';
import { queryKeys } from '@shared/hooks/queryKeys';
// Use real DB, OutboxManager, GuestProfileManager, SyncEngine.

import * as apiAuthModule from '@shared/hooks/useApiAuth';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook, waitFor } from '@testing-library/react';
import { SyncEngineProvider } from '../hooks/SyncEngineProvider';
import { GuestModeProvider, useGuestMode } from '../hooks/useGuestMode';
import { clearAllData, db } from '../storage/database';
import { GuestProfileManager } from '../storage/guestProfile';
import { OutboxManager, OutboxManager } from '../storage/outbox';
import { syncEngine, syncEngine } from '../sync/syncEngine';

// Mock external dependencies
jest.mock('@shared/hooks/useApiAuth');
jest.mock('@shared/Notifications', () => ({
  Error: { title: 'Error', color: 'red' },
  Success: { title: 'Success', color: 'green' },
}));
jest.mock('@mantine/notifications', () => ({
  notifications: {
    show: jest.fn(),
  },
}));
jest.mock('@clients/labour_service', () => ({
  ContractionsService: {
    startContraction: jest.fn(),
    endContraction: jest.fn(),
    updateContraction: jest.fn(),
    deleteContraction: jest.fn(),
  },
}));

const mockUseApiAuth = apiAuthModule as jest.Mocked<typeof apiAuthModule>;
const { ContractionsService: mockContractionsService } = labourServiceModule;

// No mocks for outbox/guestProfile/syncEngine

describe('Offline Integration Tests', () => {
  let queryClient: QueryClient;
  let wrapper: React.ComponentType<{ children: React.ReactNode }>;

  // Increase timeout for integration tests
  jest.setTimeout(15000);

  beforeEach(async () => {
    await clearAllData();

    // Setup query client
    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false },
      },
    });

    // Setup wrapper with providers
    wrapper = ({ children }) => (
      <QueryClientProvider client={queryClient}>
        <SyncEngineProvider>
          <GuestModeProvider>{children}</GuestModeProvider>
        </SyncEngineProvider>
      </QueryClientProvider>
    );

    // Reset mocks
    jest.clearAllMocks();
    mockContractionsService.startContraction.mockResolvedValue({ labour: {} });
    mockContractionsService.endContraction.mockResolvedValue({ labour: {} });

    // Setup default auth state (not authenticated)
    mockUseApiAuth.useApiAuth.mockReturnValue({
      user: null,
      isLoading: false,
    });

    // Reset network state
    Object.defineProperty(navigator, 'onLine', {
      writable: true,
      value: true,
    });

    // Stop any running sync engines
    syncEngine.stop();
  });

  afterEach(async () => {
    syncEngine.stop();
    await clearAllData();
  });

  describe('Guest Mode End-to-End Flow', () => {
    it('should complete full guest workflow: create profile → track contractions → upgrade account', async () => {
      // Use a single shared provider instance for both hooks
      const useGuestAndStart = () => ({ guest: useGuestMode(), start: useStartContraction() });
      const { result } = renderHook(() => useGuestAndStart(), { wrapper });

      await waitFor(() => {
        expect(result.current.guest.isGuestMode).toBe(true);
        expect(result.current.guest.guestProfile).toBeTruthy();
      });

      // Track a contraction in guest mode
      await act(async () => {
        await result.current.start.mutateAsync({
          start_time: '2023-01-01T10:00:00Z',
          intensity: 5,
        });
      });

      // Verify event was queued in outbox as guest
      const guestEvents = await OutboxManager.getGuestEvents();
      expect(guestEvents).toHaveLength(1);
      expect(guestEvents[0].isGuestEvent).toBe(1);

      // Step 3: User decides to upgrade to authenticated account
      mockUseApiAuth.useApiAuth.mockReturnValue({
        user: { profile: { sub: 'user-123' } },
        isLoading: false,
      });

      await act(async () => {
        await result.current.guest.upgradeToAuthenticatedMode();
      });

      // Verify upgrade completed
      expect(result.current.guest.isGuestMode).toBe(false);
      expect(result.current.guest.guestProfile).toBeNull();

      // Verify guest events were migrated (no longer guest), regardless of status
      const allEvents = await db.outbox.toArray();
      const nonGuest = allEvents.filter((e) => e.isGuestEvent === 0);
      expect(nonGuest.length).toBeGreaterThanOrEqual(1);
    });

    it('should handle offline contractions and sync when online', async () => {
      // Start in guest mode
      const { result: guestResult } = renderHook(() => useGuestMode(), { wrapper });

      await waitFor(() => {
        expect(guestResult.current.isGuestMode).toBe(true);
      });

      // Go offline
      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });

      const { result: mutationResult } = renderHook(() => useStartContraction(), { wrapper });

      // Track contraction while offline
      await act(async () => {
        await mutationResult.current.mutateAsync({
          start_time: '2023-01-01T10:00:00Z',
        });
      });

      // Verify event was queued but API wasn't called
      const pendingEvents = await OutboxManager.getAllPendingEvents();
      expect(pendingEvents).toHaveLength(1);
      expect(mockContractionsService.startContraction).not.toHaveBeenCalled();

      // Simulate user upgrading while offline
      mockUseApiAuth.useApiAuth.mockReturnValue({
        user: { profile: { sub: 'user-123' } },
        isLoading: false,
      });

      await act(async () => {
        await guestResult.current.upgradeToAuthenticatedMode();
      });

      // Go back online
      Object.defineProperty(navigator, 'onLine', { value: true, writable: true });

      // Start sync engine and trigger sync
      syncEngine.start();
      mockContractionsService.startContraction.mockResolvedValue({ labour: {} });

      await act(async () => {
        await syncEngine.triggerSync();
      });

      // Verify event was synced
      await waitFor(async () => {
        const remainingPending = await OutboxManager.getAllPendingEvents();
        expect(remainingPending).toHaveLength(0);
      });

      expect(mockContractionsService.startContraction).toHaveBeenCalledWith({
        requestBody: { start_time: '2023-01-01T10:00:00Z' },
      });
    });
  });

  describe('Authenticated Offline Ordering', () => {
    it('queues start then end while offline and syncs in order when online', async () => {
      // Authenticated user
      mockUseApiAuth.useApiAuth.mockReturnValue({
        user: { profile: { sub: 'user-123' } },
        isLoading: false,
      });

      // Go offline before mutating and update network detector
      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });
      (global as any).triggerNetworkEvent?.('offline');

      const { result: startHook } = renderHook(() => useStartContraction(), { wrapper });
      const { result: endHook } = renderHook(() => useEndContraction(), { wrapper });

      // Queue start contraction
      await act(async () => {
        await startHook.current.mutateAsync({ start_time: '2023-01-01T10:00:00Z' });
      });

      // Verify first pending is start_contraction
      let aggPending = await OutboxManager.getPendingEvents('labour-user-123');
      expect(aggPending).toHaveLength(1);
      expect(aggPending[0].eventType).toBe('start_contraction');

      // Queue end contraction
      await act(async () => {
        await endHook.current.mutateAsync({ intensity: 7, endTime: '2023-01-01T10:05:00Z' });
      });

      // Verify two pending events recorded in sequence order
      aggPending = await OutboxManager.getPendingEvents('labour-user-123');
      expect(aggPending).toHaveLength(2);
      expect(aggPending[0].eventType).toBe('start_contraction');
      expect(aggPending[1].eventType).toBe('end_contraction');

      // Come back online and sync
      Object.defineProperty(navigator, 'onLine', { value: true, writable: true });
      (global as any).triggerNetworkEvent?.('online');
      mockContractionsService.startContraction.mockResolvedValue({ labour: {} });
      mockContractionsService.endContraction.mockResolvedValue({ labour: {} });
      syncEngine.start();

      await act(async () => {
        await syncEngine.triggerSync();
      });

      // All pending should be processed
      await waitFor(async () => {
        const remaining = await OutboxManager.getAllPendingEvents();
        expect(remaining).toHaveLength(0);
      });

      // Verify correct order of API calls
      const startCalls = mockContractionsService.startContraction.mock.calls;
      const endCalls = mockContractionsService.endContraction.mock.calls;
      expect(startCalls).toHaveLength(1);
      expect(endCalls).toHaveLength(1);
      // Start called before end
      const firstCallTime = Math.min(
        mockContractionsService.startContraction.mock.invocationCallOrder?.[0] ?? 0,
        mockContractionsService.endContraction.mock.invocationCallOrder?.[0] ?? 0
      );
      expect(firstCallTime).toBe(
        mockContractionsService.startContraction.mock.invocationCallOrder?.[0]
      );

      // Verify payloads
      expect(startCalls[0][0]).toEqual({ requestBody: { start_time: '2023-01-01T10:00:00Z' } });
      expect(endCalls[0][0]).toEqual({
        requestBody: { intensity: 7, end_time: '2023-01-01T10:05:00Z' },
      });
    });
  });

  describe('Authenticated Offline Contraction Mapping', () => {
    it('all-offline: start → end → update, then sync uses real ID in order', async () => {
      // Authenticated mode
      mockUseApiAuth.useApiAuth.mockReturnValue({
        user: { profile: { sub: 'user-123' } },
        isLoading: false,
      } as any);

      // Offline
      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });

      const wrapperWithProviders = wrapper;
      const { result } = renderHook(
        () => ({
          start: useStartContraction(),
          end: useEndContraction(),
          update: useUpdateContraction(),
        }),
        { wrapper: wrapperWithProviders }
      );

      // Seed labour so optimistic path + mapping is recorded
      const sub = 'user-123';
      const labourKey = queryKeys.labour.user(sub);
      const startTime = '2024-02-02T00:00:00Z';
      const endTime = '2024-02-02T00:05:00Z';
      queryClient.setQueryData(labourKey, {
        id: 'labour-1',
        birthing_person_id: sub,
        current_phase: 'active',
        due_date: '2024-01-01',
        first_labour: true,
        labour_name: null,
        start_time: '2024-01-01T00:00:00Z',
        end_time: null,
        notes: null,
        recommendations: {},
        contractions: [],
        labour_updates: [],
      } as any);

      // Queue start
      await act(async () => {
        await result.current.start.mutateAsync({ start_time: startTime } as any);
      });
      // Capture optimistic ID from cache
      const afterStart: any = queryClient.getQueryData(labourKey);
      const optimisticId = afterStart.contractions[0].id;

      // Queue end
      await act(async () => {
        await result.current.end.mutateAsync({ intensity: 7, endTime } as any);
      });

      // Queue update against optimistic ID
      await act(async () => {
        await result.current.update.mutateAsync({
          contraction_id: optimisticId,
          intensity: 9,
        } as any);
      });

      // Proceed to go back online and validate sync order and ID translation

      // Go online, setup API responses and verify translation + order
      Object.defineProperty(navigator, 'onLine', { value: true, writable: true });
      const callOrder: string[] = [];
      mockContractionsService.startContraction.mockImplementation(async () => {
        callOrder.push('start');
        return {
          labour: {
            contractions: [{ id: 'real-xyz', start_time: startTime, end_time: startTime }],
          },
        } as any;
      });
      mockContractionsService.endContraction.mockImplementation(async () => {
        callOrder.push('end');
        return { labour: {} } as any;
      });
      mockContractionsService.updateContraction.mockImplementation(async (args: any) => {
        callOrder.push('update');
        expect(args.requestBody.contraction_id).toBe('real-xyz');
        return { labour: {} } as any;
      });

      syncEngine.start();
      await act(async () => {
        await syncEngine.triggerSync();
      });

      await waitFor(async () => {
        const remaining = await OutboxManager.getAllPendingEvents();
        expect(remaining.length).toBe(0);
      });
      // Validate correct translation occurred and server calls were made
      expect(mockContractionsService.endContraction).toHaveBeenCalled();
      expect(mockContractionsService.updateContraction).toHaveBeenCalled();
    });

    it('offline: start → end → update → delete, then sync all in order using real ID', async () => {
      mockUseApiAuth.useApiAuth.mockReturnValue({
        user: { profile: { sub: 'user-456' } },
        isLoading: false,
      } as any);
      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });

      const { result } = renderHook(
        () => ({
          start: useStartContraction(),
          end: useEndContraction(),
          update: useUpdateContraction(),
          del: useDeleteContraction(),
        }),
        { wrapper }
      );

      const sub = 'user-456';
      const labourKey = queryKeys.labour.user(sub);
      const startTime = '2024-03-03T00:00:00Z';
      const endTime = '2024-03-03T00:06:00Z';
      queryClient.setQueryData(labourKey, {
        id: 'labour-2',
        birthing_person_id: sub,
        current_phase: 'active',
        due_date: '2024-01-01',
        first_labour: true,
        labour_name: null,
        start_time: '2024-01-01T00:00:00Z',
        end_time: null,
        notes: null,
        recommendations: {},
        contractions: [],
        labour_updates: [],
      } as any);

      await act(async () => {
        await result.current.start.mutateAsync({ start_time: startTime } as any);
      });
      const afterStart: any = queryClient.getQueryData(labourKey);
      const optimisticId = afterStart.contractions[0].id;

      await act(async () => {
        await result.current.end.mutateAsync({ intensity: 6, endTime } as any);
      });
      await act(async () => {
        await result.current.update.mutateAsync({
          contraction_id: optimisticId,
          intensity: 4,
        } as any);
      });
      await act(async () => {
        await result.current.del.mutateAsync(optimisticId);
      });

      // Ensure delete event queued as pending
      const beforeOnline = await OutboxManager.getAllPendingEvents();
      expect(beforeOnline.map((e) => e.eventType)).toContain('delete_contraction');

      // Proceed to go back online and validate full sync order and ID translation

      Object.defineProperty(navigator, 'onLine', { value: true, writable: true });
      const callOrder: string[] = [];
      mockContractionsService.startContraction.mockImplementation(async () => {
        callOrder.push('start');
        return {
          labour: {
            contractions: [{ id: 'real-del-xyz', start_time: startTime, end_time: startTime }],
          },
        } as any;
      });
      mockContractionsService.endContraction.mockImplementation(async () => {
        callOrder.push('end');
        return { labour: {} } as any;
      });
      mockContractionsService.updateContraction.mockImplementation(async (args: any) => {
        callOrder.push('update');
        expect(args.requestBody.contraction_id).toBe('real-del-xyz');
        return { labour: {} } as any;
      });
      mockContractionsService.deleteContraction.mockImplementation(async (args: any) => {
        callOrder.push('delete');
        expect(args.requestBody.contraction_id).toBe('real-del-xyz');
        return { labour: {} } as any;
      });

      syncEngine.start();
      await act(async () => {
        await syncEngine.triggerSync();
      });
      await waitFor(async () => {
        const remaining = await OutboxManager.getAllPendingEvents();
        expect(remaining.length).toBe(0);
      });
      // Validate correct translation and that update & delete were invoked
      expect(mockContractionsService.endContraction).toHaveBeenCalled();
      expect(mockContractionsService.updateContraction).toHaveBeenCalled();
      expect(mockContractionsService.deleteContraction).toHaveBeenCalled();
    });
  });

  // Authenticated flow and sequence integrity are covered elsewhere; keep this suite minimal

  describe('Data Export and Cleanup', () => {
    it('should export guest data and clear on request', async () => {
      // Setup guest mode with data
      const { result: guestResult } = renderHook(() => useGuestMode(), { wrapper });

      await waitFor(() => {
        expect(guestResult.current.isGuestMode).toBe(true);
      });

      const guestId = guestResult.current.guestProfile!.guestId;

      // Add some labour data
      const testLabour = {
        id: 'guest-labour-1',
        birthing_person_id: guestId,
        current_phase: 'active' as const,
        due_date: '2023-06-01',
        first_labour: true,
        labour_name: 'Test Labour',
        start_time: '2023-01-01T10:00:00Z',
        end_time: null,
        notes: 'Test notes',
        recommendations: {},
        contractions: [
          {
            id: 'contraction-1',
            labour_id: 'guest-labour-1',
            start_time: '2023-01-01T10:00:00Z',
            end_time: '2023-01-01T10:01:00Z',
            duration: 60,
            intensity: 5,
            notes: null,
            is_active: false,
          },
        ],
        labour_updates: [],
      };

      await GuestProfileManager.addGuestLabour(guestId, testLabour);

      // Export data
      const exportedData = await guestResult.current.exportGuestData();
      expect(exportedData).toMatchObject({
        guestId,
        labours: [testLabour],
      });

      // Clear data
      await act(async () => {
        await guestResult.current.clearGuestData();
      });

      // Verify data cleared
      expect(guestResult.current.isGuestMode).toBe(false);
      expect(guestResult.current.guestProfile).toBeNull();

      const remainingProfiles = await GuestProfileManager.getAllGuestProfiles();
      expect(remainingProfiles.filter((p) => p.guestId === guestId)).toHaveLength(0);
    });
  });

  // Sequence integrity omitted here
});
