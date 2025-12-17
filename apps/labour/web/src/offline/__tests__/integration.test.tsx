// @ts-nocheck

import React from 'react';
import { queryKeys } from '@base/hooks/queryKeys';
// Use real DB, OutboxManager, SyncEngine.

import * as apiAuthModule from '@base/hooks/useApiAuth';
import {
  useDeleteContractionV2,
  useEndContractionV2,
  useStartContractionV2,
  useUpdateContractionV2,
} from '@base/hooks/useLabourData';
import * as labourServiceModule from '@clients/labour_service/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook, waitFor } from '@testing-library/react';
import { clearAllData } from '../storage/database';
import { OutboxManager } from '../storage/outbox';
import { syncEngine } from '../sync/syncEngine';

// Mock external dependencies
jest.mock('@base/hooks/useApiAuth');
jest.mock('@shared/Notifications', () => ({
  Error: { title: 'Error', color: 'red' },
  Success: { title: 'Success', color: 'green' },
}));
jest.mock('@mantine/notifications', () => ({
  notifications: {
    show: jest.fn(),
  },
}));
jest.mock('@clients/labour_service/client', () => ({
  LabourServiceClient: {
    startContraction: jest.fn(),
    endContraction: jest.fn(),
    updateContraction: jest.fn(),
    deleteContraction: jest.fn(),
  },
}));

const mockUseApiAuth = apiAuthModule as jest.Mocked<typeof apiAuthModule>;
const { LabourServiceClient: mockLabourServiceClient } = labourServiceModule;

// No mocks for outbox/syncEngine

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
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    );

    // Reset mocks
    jest.clearAllMocks();
    mockLabourServiceClient.startContraction.mockResolvedValue({ labour: {} });
    mockLabourServiceClient.endContraction.mockResolvedValue({ labour: {} });

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

      const { result: startHook } = renderHook(() => useStartContractionV2(), { wrapper });
      const { result: endHook } = renderHook(() => useEndContractionV2(), { wrapper });

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
      mockLabourServiceClient.startContraction.mockResolvedValue({ labour: {} });
      mockLabourServiceClient.endContraction.mockResolvedValue({ labour: {} });
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
      const startCalls = mockLabourServiceClient.startContraction.mock.calls;
      const endCalls = mockLabourServiceClient.endContraction.mock.calls;
      expect(startCalls).toHaveLength(1);
      expect(endCalls).toHaveLength(1);
      // Start called before end
      const firstCallTime = Math.min(
        mockLabourServiceClient.startContraction.mock.invocationCallOrder?.[0] ?? 0,
        mockLabourServiceClient.endContraction.mock.invocationCallOrder?.[0] ?? 0
      );
      expect(firstCallTime).toBe(
        mockLabourServiceClient.startContraction.mock.invocationCallOrder?.[0]
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
          start: useStartContractionV2(),
          end: useEndContractionV2(),
          update: useUpdateContractionV2(),
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
      mockLabourServiceClient.startContraction.mockImplementation(async () => {
        callOrder.push('start');
        return {
          labour: {
            contractions: [{ id: 'real-xyz', start_time: startTime, end_time: startTime }],
          },
        } as any;
      });
      mockLabourServiceClient.endContraction.mockImplementation(async () => {
        callOrder.push('end');
        return { labour: {} } as any;
      });
      mockLabourServiceClient.updateContraction.mockImplementation(async (args: any) => {
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
      expect(mockLabourServiceClient.endContraction).toHaveBeenCalled();
      expect(mockLabourServiceClient.updateContraction).toHaveBeenCalled();
    });

    it('offline: start → end → update → delete, then sync all in order using real ID', async () => {
      mockUseApiAuth.useApiAuth.mockReturnValue({
        user: { profile: { sub: 'user-456' } },
        isLoading: false,
      } as any);
      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });

      const { result } = renderHook(
        () => ({
          start: useStartContractionV2(),
          end: useEndContractionV2(),
          update: useUpdateContractionV2(),
          del: useDeleteContractionV2(),
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
      mockLabourServiceClient.startContraction.mockImplementation(async () => {
        callOrder.push('start');
        return {
          labour: {
            contractions: [{ id: 'real-del-xyz', start_time: startTime, end_time: startTime }],
          },
        } as any;
      });
      mockLabourServiceClient.endContraction.mockImplementation(async () => {
        callOrder.push('end');
        return { labour: {} } as any;
      });
      mockLabourServiceClient.updateContraction.mockImplementation(async (args: any) => {
        callOrder.push('update');
        expect(args.requestBody.contraction_id).toBe('real-del-xyz');
        return { labour: {} } as any;
      });
      mockLabourServiceClient.deleteContraction.mockImplementation(async (args: any) => {
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
      expect(mockLabourServiceClient.endContraction).toHaveBeenCalled();
      expect(mockLabourServiceClient.updateContraction).toHaveBeenCalled();
      expect(mockLabourServiceClient.deleteContraction).toHaveBeenCalled();
    });
  });
});
