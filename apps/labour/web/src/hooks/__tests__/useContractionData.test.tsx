// @ts-nocheck
import 'fake-indexeddb/auto';

import React from 'react';
import * as apiAuthModule from '@base/hooks/useApiAuth';
import * as useLabourClientModule from '@base/hooks/useLabourClient';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook, waitFor } from '@testing-library/react';
import { clearAllData, db } from '../../offline/storage/database';
import { OutboxManager } from '../../offline/storage/outbox';
import { queryKeysV2 } from '../queryKeys';
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

const mockClient = {
  startContraction: jest.fn(),
  updateContraction: jest.fn(),
  deleteContraction: jest.fn(),
};

jest.mock('@base/hooks/useLabourClient', () => ({
  useLabourV2Client: jest.fn(() => mockClient),
}));

const mockUseApiAuth = apiAuthModule as jest.Mocked<typeof apiAuthModule>;

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
    mockClient.startContraction.mockResolvedValue({ success: true, data: {} });
    mockClient.updateContraction.mockResolvedValue({ success: true, data: {} });
    mockClient.deleteContraction.mockResolvedValue({ success: true, data: {} });
    Object.defineProperty(navigator, 'onLine', { value: true, writable: true });
  });

  afterEach(async () => {
    await clearAllData();
  });

  it('records temp mapping on start mutate', async () => {
    const { result } = renderHook(() => useStartContractionV2(mockClient as any), { wrapper });
    const startTime = '2024-01-01T00:00:00Z';

    // Seed cache with current labour to enable optimistic path and mapping
    const sub = 'user-abc';
    queryClient.setQueryData(queryKeysV2.labour.active(sub), {
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
    const { result: startHook } = renderHook(() => useUpdateContractionV2(mockClient as any), { wrapper });

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

    queryClient.setQueryData(queryKeysV2.labour.active(sub), labour);

    await expect(
      act(async () => {
        await startHook.current.mutateAsync({ contraction_id: 'active-1', intensity: 7 } as any);
      })
    ).rejects.toBeDefined();

    const pending = await OutboxManager.getAllPendingEvents();
    expect(pending.length).toBe(0);
  });

  it('prevents deleting an in-progress contraction (authenticated)', async () => {
    const { result } = renderHook(() => useDeleteContractionV2(mockClient as any), { wrapper });
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
    queryClient.setQueryData(queryKeysV2.labour.active(sub), labour);

    await expect(
      act(async () => {
        await result.current.mutateAsync('active-2');
      })
    ).rejects.toBeDefined();

    const pending = await OutboxManager.getAllPendingEvents();
    expect(pending.length).toBe(0);
  });

  it('allows updating a completed contraction (authenticated)', async () => {
    const { result } = renderHook(() => useUpdateContractionV2(mockClient as any), { wrapper });
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
    queryClient.setQueryData(queryKeysV2.labour.active(sub), labour);

    mockClient.updateContraction.mockResolvedValue({ success: true, data: labour });

    await act(async () => {
      await result.current.mutateAsync({ contraction_id: 'ended-1', intensity: 8 } as any);
    });
    expect(mockClient.updateContraction).toHaveBeenCalledTimes(1);
  });

  it('allows deleting a completed contraction (authenticated)', async () => {
    const { result } = renderHook(() => useDeleteContractionV2(mockClient as any), { wrapper });
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
    queryClient.setQueryData(queryKeysV2.labour.active(sub), labour);

    mockClient.deleteContraction.mockResolvedValue({ success: true, data: labour });

    await act(async () => {
      await result.current.mutateAsync('ended-2');
    });
    expect(mockClient.deleteContraction).toHaveBeenCalledTimes(1);
  });
});
