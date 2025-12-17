// @ts-nocheck

import React from 'react';
import * as apiAuthModule from '@base/hooks/useApiAuth';
import * as labourServiceModule from '@clients/labour_service/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook, waitFor } from '@testing-library/react';
import { clearAllData } from '../../storage/database';
import { OutboxManager } from '../../storage/outbox';
import { syncEngine } from '../../sync/syncEngine';
import { useOfflineMutation, useOnlineMutation } from '../useOfflineMutation';

// Use real storage/sync layers. Only mock auth and external API clients.
jest.mock('@base/hooks/useApiAuth');

jest.mock('@clients/labour_service/client', () => ({
  LabourServiceClient: jest.fn().mockImplementation(() => ({
    startContraction: jest.fn(),
    endContraction: jest.fn(),
    updateContraction: jest.fn(),
    deleteContraction: jest.fn(),
    planLabour: jest.fn(),
    completeLabour: jest.fn(),
    postLabourUpdate: jest.fn(),
  })),
}));

jest.mock('@base/hooks/useLabourClient', () => ({
  useLabourV2Client: () => ({
    startContraction: jest.fn(),
    updateContraction: jest.fn(),
    deleteContraction: jest.fn(),
    getActiveLabour: jest.fn(),
    getLabour: jest.fn(),
    getLabourHistory: jest.fn(),
    getContractions: jest.fn(),
    getContractionById: jest.fn(),
    getLabourUpdates: jest.fn(),
    getLabourUpdateById: jest.fn(),
    endContraction: jest.fn(),
    updateLabourUpdateMessage: jest.fn(),
    updateLabourUpdateType: jest.fn(),
    postLabourUpdate: jest.fn(),
    deleteLabourUpdate: jest.fn(),
    planLabour: jest.fn(),
    updateLabourPlan: jest.fn(),
    beginLabour: jest.fn(),
    completeLabour: jest.fn(),
    deleteLabour: jest.fn(),
    sendLabourInvite: jest.fn(),
    getSubscriptionToken: jest.fn(),
    getLabourSubscriptions: jest.fn(),
    getUserSubscription: jest.fn(),
    getSubscribedLabours: jest.fn(),
    getUserSubscriptions: jest.fn(),
    getUsers: jest.fn(),
    requestAccess: jest.fn(),
    unsubscribe: jest.fn(),
    updateNotificationMethods: jest.fn(),
    updateAccessLevel: jest.fn(),
    approveSubscriber: jest.fn(),
    removeSubscriber: jest.fn(),
    blockSubscriber: jest.fn(),
    unblockSubscriber: jest.fn(),
    updateSubscriberRole: jest.fn(),
  }),
}));

// Prevent background state updates in tests from useSyncEngine interval
jest.mock('../useSyncEngine', () => ({
  useSyncEngine: () => ({
    triggerSync: jest.fn(),
    retryFailedEvents: jest.fn(),
    pruneSyncedEvents: jest.fn(),
    syncStatus: {
      isRunning: false,
      isOnline: true,
      pendingEvents: 0,
      syncingEvents: 0,
      failedEvents: 0,
      activeSyncs: 0,
      scheduledRetries: 0,
    },
  }),
}));

const mockUseApiAuth = apiAuthModule as jest.Mocked<typeof apiAuthModule>;
const { LabourServiceClient: mockLabourServiceClient } = labourServiceModule;

// Ensure navigator.onLine is controllable
Object.defineProperty(navigator, 'onLine', { value: true, writable: true });

describe('useOfflineMutation (integration)', () => {
  let queryClient: QueryClient;
  let wrapper: React.ComponentType<{ children: React.ReactNode }>;

  beforeEach(async () => {
    await clearAllData();
    syncEngine.stop();

    queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
        mutations: { retry: false },
      },
    });

    wrapper = ({ children }) => (
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    );

    jest.clearAllMocks();
    (labourServiceModule.LabourServiceClient as jest.Mock).mockImplementation(() => ({
      startContraction: jest.fn().mockResolvedValue({ success: true, data: { labour: {} } }),
      endContraction: jest.fn().mockResolvedValue({ success: true, data: { labour: {} } }),
      updateContraction: jest.fn().mockResolvedValue({ success: true, data: { labour: {} } }),
      deleteContraction: jest.fn().mockResolvedValue({ success: true, data: {} }),
      planLabour: jest.fn().mockResolvedValue({ success: true, data: { labour: {} } }),
      completeLabour: jest.fn().mockResolvedValue({ success: true, data: {} }),
      postLabourUpdate: jest.fn().mockResolvedValue({ success: true, data: { labour_update: {} } }),
    }));
    // Default to authenticated user (non-guest)
    mockUseApiAuth.useApiAuth.mockReturnValue({
      isAuthenticated: true,
      isLoading: false,
      user: { profile: { sub: 'user-123' } } as any,
      accessToken: 'token',
    } as any);
    Object.defineProperty(navigator, 'onLine', { value: true, writable: true });
  });

  afterEach(async () => {
    syncEngine.stop();
    await clearAllData();
  });

  it('queues event and executes mutation when online (non-guest)', async () => {
    const mutationFn = jest.fn().mockResolvedValue('success');
    const onSuccess = jest.fn();

    const { result } = renderHook(
      () =>
        useOfflineMutation<any, Error, any>({
          eventType: 'start_contraction',
          getAggregateId: () => 'labour-1',
          mutationFn,
          onSuccess,
        }),
      { wrapper }
    );

    await act(async () => {
      await result.current.mutateAsync({ test: 'data' });
    });

    const pending = await OutboxManager.getAllPendingEvents();
    // Event is pruned after successful online mutation
    expect(pending.length).toBe(0);
    expect(mutationFn).toHaveBeenCalledWith({ test: 'data' });
    expect(onSuccess).toHaveBeenCalledWith('success', { test: 'data' }, undefined);
  });

  it('triggers sync when online mutation fails (queued event should be retried)', async () => {
    // Mock useSyncEngine to capture triggerSync
    const useSyncEngineModule = await import('../useSyncEngine');
    const triggerSyncSpy = jest.fn();
    useSyncEngineModule.useSyncEngine = () => ({
      triggerSync: triggerSyncSpy,
      retryFailedEvents: jest.fn(),
      pruneSyncedEvents: jest.fn(),
      syncStatus: {
        isRunning: true,
        isOnline: true,
        pendingEvents: 0,
        syncingEvents: 0,
        failedEvents: 0,
        activeSyncs: 0,
        scheduledRetries: 0,
      },
    });

    const mutationFn = jest.fn().mockRejectedValue(new Error('Network error'));
    const onError = jest.fn();

    const { result } = renderHook(
      () =>
        useOfflineMutation<any, Error, any>({
          eventType: 'start_contraction',
          getAggregateId: () => 'labour-1',
          mutationFn,
          onError,
        }),
      { wrapper }
    );

    await act(async () => {
      await expect(result.current.mutateAsync({ test: 'data' })).rejects.toThrow('Network error');
    });

    expect(triggerSyncSpy).toHaveBeenCalled();
    const pending = await OutboxManager.getAllPendingEvents();
    expect(pending.length).toBeGreaterThanOrEqual(1);
  });

  it('queues event and does not call mutation when offline', async () => {
    Object.defineProperty(navigator, 'onLine', { value: false, writable: true });

    const mutationFn = jest.fn();
    const { result } = renderHook(
      () =>
        useOfflineMutation<any, Error, any>({
          eventType: 'start_contraction',
          getAggregateId: () => 'labour-1',
          mutationFn,
        }),
      { wrapper }
    );

    await act(async () => {
      await result.current.mutateAsync({ start_time: '2023-01-01T00:00:00Z' });
    });

    const pending = await OutboxManager.getAllPendingEvents();
    expect(pending.length).toBe(1);
    expect(mutationFn).not.toHaveBeenCalled();
  });

  it('skipOutbox: does not queue event and calls mutation', async () => {
    const mutationFn = jest.fn().mockResolvedValue('ok');

    const { result } = renderHook(
      () =>
        useOfflineMutation<any, Error, any>({
          eventType: 'start_contraction',
          getAggregateId: () => 'labour-1',
          mutationFn,
          skipOutbox: true,
        }),
      { wrapper }
    );

    await act(async () => {
      await result.current.mutateAsync({ foo: 'bar' });
    });

    const pending = await OutboxManager.getAllPendingEvents();
    expect(pending.length).toBe(0);
    expect(mutationFn).toHaveBeenCalledWith({ foo: 'bar' });
  });

  it('uses custom payload extraction (offline)', async () => {
    Object.defineProperty(navigator, 'onLine', { value: false, writable: true });
    const getPayload = jest.fn().mockReturnValue({ custom: 'payload' });
    const { result } = renderHook(
      () =>
        useOfflineMutation<any, Error, any>({
          eventType: 'start_contraction',
          getAggregateId: () => 'labour-1',
          mutationFn: async () => 'ok' as any,
          getPayload,
        }),
      { wrapper }
    );

    await act(async () => {
      await result.current.mutateAsync({ any: 'thing' });
    });

    expect(getPayload).toHaveBeenCalledWith({ any: 'thing' });
    const pending = await OutboxManager.getAllPendingEvents();
    expect(pending[0].payload).toEqual({ custom: 'payload' });
  });

  it('sync integration: queues offline then engine processes when online', async () => {
    mockUseApiAuth.useApiAuth.mockReturnValue({
      user: { profile: { sub: 'user-123' } },
      isLoading: false,
    });
    Object.defineProperty(navigator, 'onLine', { value: false, writable: true });

    const { result } = renderHook(
      () =>
        useOfflineMutation<any, Error, any>({
          eventType: 'start_contraction',
          getAggregateId: () => 'labour-1',
          mutationFn: async () => 'ok' as any,
        }),
      { wrapper }
    );

    await act(async () => {
      await result.current.mutateAsync({ start_time: '2023-01-01T00:00:00Z' });
    });

    const pending = await OutboxManager.getAllPendingEvents();
    expect(pending.length).toBe(1);

    Object.defineProperty(navigator, 'onLine', { value: true, writable: true });
    syncEngine.start();
    await act(async () => {
      await syncEngine.triggerSync();
    });

    await waitFor(async () => {
      const remaining = await OutboxManager.getAllPendingEvents();
      expect(remaining.length).toBe(0);
    });

    expect(mockLabourServiceClient.startContraction).toHaveBeenCalledWith({
      requestBody: { start_time: '2023-01-01T00:00:00Z' },
    });
  });
});

describe('useOnlineMutation (integration)', () => {
  let queryClient: QueryClient;
  let wrapper: React.ComponentType<{ children: React.ReactNode }>;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
    });

    wrapper = ({ children }) => (
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    );
  });

  it('executes mutation and calls onSettled', async () => {
    const mutationFn = jest.fn().mockResolvedValue('success');
    const onSuccess = jest.fn();

    const { result } = renderHook(
      () => useOnlineMutation<any, Error, any>({ mutationFn, onSuccess }),
      { wrapper }
    );

    await act(async () => {
      await result.current.mutateAsync({ test: 'data' });
    });

    expect(mutationFn).toHaveBeenCalledWith({ test: 'data' });
    expect(onSuccess).toHaveBeenCalledWith('success', { test: 'data' }, undefined);
  });
});
