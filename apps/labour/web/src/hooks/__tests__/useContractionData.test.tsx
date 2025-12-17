// @ts-nocheck
import 'fake-indexeddb/auto';

import React from 'react';
import * as apiAuthModule from '@base/hooks/useApiAuth';
import * as labourServiceModule from '@clients/labour_service/client';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook, waitFor } from '@testing-library/react';
import { clearAllData, db } from '../../offline/storage/database';
import { OutboxManager } from '../../offline/storage/outbox';
import { queryKeys } from '../queryKeys';
import {
  useDeleteContractionV2,
  useStartContractionV2,
  useUpdateContractionV2,
} from '../useLabourData';

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
jest.mock('@clients/labour_service', () => ({
  LabourServiceClient: {
    startContraction: jest.fn(),
    updateContraction: jest.fn(),
    deleteContraction: jest.fn(),
  },
}));

const mockUseApiAuth = apiAuthModule as jest.Mocked<typeof apiAuthModule>;
const { LabourServiceClient: mockLabourServiceClient } = labourServiceModule;

describe('useContractionData mapping', () => {
  let queryClient: QueryClient;
  let wrapper: React.ComponentType<{ children: React.ReactNode }>;

  beforeEach(async () => {
    await clearAllData();
    queryClient = new QueryClient({
      defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
    });
    wrapper = ({ children }) => (
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    );
    jest.clearAllMocks();
    mockUseApiAuth.useApiAuth.mockReturnValue({ user: { profile: { sub: 'user-abc' } } } as any);
    mockLabourServiceClient.startContraction.mockResolvedValue({ labour: {} });
    Object.defineProperty(navigator, 'onLine', { value: true, writable: true });
  });

  afterEach(async () => {
    await clearAllData();
  });

  it('records temp mapping on start mutate', async () => {
    const { result } = renderHook(() => useStartContractionV2(), { wrapper });
    const startTime = '2024-01-01T00:00:00Z';

    // Seed cache with current labour to enable optimistic path and mapping
    const sub = 'user-abc';
    queryClient.setQueryData(queryKeys.labour.user(sub), {
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

    await act(async () => {
      await result.current.mutateAsync({ start_time: startTime, intensity: 5 } as any);
    });

    // Verify a mapping exists for this aggregate and start time (allow async write to settle)
    const aggregateId = 'labour-user-abc';
    await waitFor(async () => {
      const matches = await db.contractionIdMap
        .where('[aggregateId+startTime]')
        .equals([aggregateId, startTime])
        .toArray();
      expect(matches.length).toBeGreaterThan(0);
    });
  });

  it('prevents updating an in-progress contraction (authenticated)', async () => {
    const { result: startHook } = renderHook(() => useUpdateContractionV2(), { wrapper });

    const sub = 'user-abc';
    const labour = {
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
      contractions: [
        {
          id: 'active-1',
          labour_id: 'labour-1',
          start_time: '2024-01-01T01:00:00Z',
          end_time: '2024-01-01T01:00:00Z',
          duration: 0,
          intensity: 5,
          notes: null,
          is_active: true,
        },
      ],
      labour_updates: [],
    } as any;

    queryClient.setQueryData(queryKeys.labour.user(sub), labour);

    await expect(
      act(async () => {
        await startHook.current.mutateAsync({ contraction_id: 'active-1', intensity: 7 } as any);
      })
    ).rejects.toBeDefined();

    const pending = await OutboxManager.getAllPendingEvents();
    expect(pending.length).toBe(0);
  });

  it('prevents deleting an in-progress contraction (authenticated)', async () => {
    const { result } = renderHook(() => useDeleteContractionV2(), { wrapper });
    const sub = 'user-abc';
    const labour = {
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
      contractions: [
        {
          id: 'active-2',
          labour_id: 'labour-1',
          start_time: '2024-01-01T01:00:00Z',
          end_time: '2024-01-01T01:00:00Z',
          duration: 0,
          intensity: 5,
          notes: null,
          is_active: true,
        },
      ],
      labour_updates: [],
    } as any;
    queryClient.setQueryData(queryKeys.labour.user(sub), labour);

    await expect(
      act(async () => {
        await result.current.mutateAsync('active-2');
      })
    ).rejects.toBeDefined();

    const pending = await OutboxManager.getAllPendingEvents();
    expect(pending.length).toBe(0);
  });

  it('allows updating a completed contraction (authenticated)', async () => {
    const { result } = renderHook(() => useUpdateContractionV2(), { wrapper });
    const sub = 'user-abc';
    const labour = {
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
      contractions: [
        {
          id: 'ended-1',
          labour_id: 'labour-1',
          start_time: '2024-01-01T01:00:00Z',
          end_time: '2024-01-01T01:05:00Z',
          duration: 300,
          intensity: 5,
          notes: null,
          is_active: false,
        },
      ],
      labour_updates: [],
    } as any;
    queryClient.setQueryData(queryKeys.labour.user(sub), labour);

    mockLabourServiceClient.updateContraction.mockResolvedValue({ labour });

    await act(async () => {
      await result.current.mutateAsync({ contraction_id: 'ended-1', intensity: 8 } as any);
    });
    expect(mockLabourServiceClient.updateContraction).toHaveBeenCalledTimes(1);
    expect(
      mockLabourServiceClient.updateContraction.mock.calls[0][0].requestBody.contraction_id
    ).toBe('ended-1');
  });

  it('allows deleting a completed contraction (authenticated)', async () => {
    const { result } = renderHook(() => useDeleteContractionV2(), { wrapper });
    const sub = 'user-abc';
    const labour = {
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
      contractions: [
        {
          id: 'ended-2',
          labour_id: 'labour-1',
          start_time: '2024-01-01T01:00:00Z',
          end_time: '2024-01-01T01:05:00Z',
          duration: 300,
          intensity: 5,
          notes: null,
          is_active: false,
        },
      ],
      labour_updates: [],
    } as any;
    queryClient.setQueryData(queryKeys.labour.user(sub), labour);

    mockLabourServiceClient.deleteContraction.mockResolvedValue({ labour });

    await act(async () => {
      await result.current.mutateAsync('ended-2');
    });
    expect(mockLabourServiceClient.deleteContraction).toHaveBeenCalledTimes(1);
    expect(
      mockLabourServiceClient.deleteContraction.mock.calls[0][0].requestBody.contraction_id
    ).toBe('ended-2');
  });
});
