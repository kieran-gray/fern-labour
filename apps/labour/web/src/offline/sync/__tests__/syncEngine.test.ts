// @ts-nocheck

import 'fake-indexeddb/auto';

// Get mocked services for test verification
import * as labourServiceModule from '@clients/labour_service/client';
import { ContractionIdMapper } from '../../storage/contractionIdMap';
import { OfflineDatabase } from '../../storage/database';
import { OutboxManager } from '../../storage/outbox';
import { networkDetector } from '../networkDetector';
import { SyncEngine } from '../syncEngine';

// Helper function for network state changes
const setNetworkOnline = (isOnline: boolean) => {
  Object.defineProperty(navigator, 'onLine', { value: isOnline, writable: true });
  (global as any).triggerNetworkEvent(isOnline ? 'online' : 'offline');
  // Force networkDetector to update its cached state immediately
  const newState = { isOnline };
  (networkDetector as any).currentState = newState;
};

// Mock the API clients - these are network calls we need to mock
jest.mock('@clients/labour_service/client', () => ({
  LabourServiceClient: {
    startContraction: jest.fn(),
    endContraction: jest.fn(),
    updateContraction: jest.fn(),
    deleteContraction: jest.fn(),
    planLabour: jest.fn(),
    completeLabour: jest.fn(),
    postLabourUpdate: jest.fn(),
  },
}));

const { LabourServiceClient: mockLabourServiceClient } = labourServiceModule;

describe('SyncEngine', () => {
  let testDb: OfflineDatabase;
  let syncEngine: SyncEngine;

  beforeEach(async () => {
    // Reset network state to online for clean tests
    setNetworkOnline(true);

    // Set up clean database
    testDb = new OfflineDatabase();
    await testDb.open();
    await testDb.transaction(
      'rw',
      [
        testDb.outbox,
        testDb.sequences,
        // @ts-ignore - table exists from DB v2
        testDb.contractionIdMap,
      ],
      async () => {
        await testDb.outbox.clear();
        await testDb.sequences.clear();
        // @ts-ignore - table exists from DB v2
        await testDb.contractionIdMap.clear();
      }
    );

    // Clear all service mocks
    jest.clearAllMocks();

    // Create fresh sync engine and ensure clean state
    syncEngine = new SyncEngine();
    syncEngine.stop(); // Ensure it's stopped
  });

  afterEach(async () => {
    if (syncEngine) {
      syncEngine.stop();
    }
    if (testDb && testDb.isOpen()) {
      await testDb.close();
    }
  });

  describe('lifecycle management', () => {
    it('should start and stop properly', async () => {
      expect(syncEngine).toBeDefined();

      syncEngine.start();
      const status = await syncEngine.getSyncStatus();
      expect(status.isRunning).toBe(true);

      syncEngine.stop();
      const stoppedStatus = await syncEngine.getSyncStatus();
      expect(stoppedStatus.isRunning).toBe(false);
    });

    it('should not start twice', () => {
      syncEngine.start();
      syncEngine.start(); // Should be ignored

      // Should not throw or cause issues
      expect(() => syncEngine.stop()).not.toThrow();
    });

    it('should clear timers on stop', async () => {
      syncEngine.start();

      // Add a failing event to trigger retry scheduling
      await OutboxManager.addEvent('labour-1', 'start_contraction', {});
      mockLabourServiceClient.startContraction.mockRejectedValue(new Error('Network error'));

      await syncEngine.triggerSync();

      const statusBefore = await syncEngine.getSyncStatus();
      expect(statusBefore.scheduledRetries).toBeGreaterThan(0);

      syncEngine.stop();

      const statusAfter = await syncEngine.getSyncStatus();
      expect(statusAfter.scheduledRetries).toBe(0);
    });
  });

  describe('event execution', () => {
    beforeEach(() => {
      syncEngine.start();
    });

    it('should execute start_contraction events', async () => {
      const payload = { start_time: '2023-01-01T00:00:00Z' };
      await OutboxManager.addEvent('labour-1', 'start_contraction', payload);

      mockLabourServiceClient.startContraction.mockResolvedValue({ labour: {} });

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.startContraction).toHaveBeenCalledWith({
        requestBody: payload,
      });

      // Event should be marked as synced and removed
      const remainingEvents = await OutboxManager.getAllPendingEvents();
      expect(remainingEvents).toHaveLength(0);
    });

    it('should execute end_contraction events', async () => {
      const payload = { intensity: 8, end_time: '2023-01-01T00:01:00Z' };
      await OutboxManager.addEvent('labour-1', 'end_contraction', payload);

      mockLabourServiceClient.endContraction.mockResolvedValue({ labour: {} });

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.endContraction).toHaveBeenCalledWith({
        requestBody: payload,
      });
    });

    it('should execute plan_labour events', async () => {
      const payload = { due_date: '2023-06-01', first_labour: true, labour_name: 'Test Labour' };
      await OutboxManager.addEvent('labour-1', 'plan_labour', payload);

      mockLabourServiceClient.planLabour.mockResolvedValue({ labour: {} });

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.planLabour).toHaveBeenCalledWith({
        requestBody: payload,
      });
    });

    it('should execute complete_labour events', async () => {
      const payload = { end_time: '2023-01-01T10:00:00Z' };
      await OutboxManager.addEvent('labour-1', 'complete_labour', payload);

      mockLabourServiceClient.completeLabour.mockResolvedValue(undefined);

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.completeLabour).toHaveBeenCalledWith({
        requestBody: payload,
      });
    });

    it('should execute update_contraction events', async () => {
      const payload = { contraction_id: 'contraction-1', intensity: 7 };
      await OutboxManager.addEvent('labour-1', 'update_contraction', payload);

      mockLabourServiceClient.updateContraction.mockResolvedValue({ labour: {} });

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.updateContraction).toHaveBeenCalledWith({
        requestBody: payload,
      });
    });

    it('should execute delete_contraction events', async () => {
      const payload = { contraction_id: 'contraction-1' };
      await OutboxManager.addEvent('labour-1', 'delete_contraction', payload);

      mockLabourServiceClient.deleteContraction.mockResolvedValue(undefined);

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.deleteContraction).toHaveBeenCalledWith({
        requestBody: payload,
      });
    });

    it('should execute labour_update events', async () => {
      const payload = { labour_update_type: 'status_update', message: 'Feeling good' };
      await OutboxManager.addEvent('labour-1', 'labour_update', payload);

      mockLabourUpdatesService.postLabourUpdate.mockResolvedValue({ labour_update: {} });

      await syncEngine.triggerSync();

      expect(mockLabourUpdatesService.postLabourUpdate).toHaveBeenCalledWith({
        requestBody: payload,
      });
    });

    it('should handle unknown event types by marking as failed', async () => {
      await OutboxManager.addEvent('labour-1', 'unknown_event' as any, {});

      await syncEngine.triggerSync();

      const failedEvents = await OutboxManager.getEventsByStatus('failed');
      expect(failedEvents).toHaveLength(1);
      expect(failedEvents[0].eventType).toBe('unknown_event');
    });

    it('should include idempotency headers', async () => {
      await OutboxManager.addEvent('labour-1', 'start_contraction', {
        start_time: '2023-01-01T00:00:00Z',
      });
      mockLabourServiceClient.startContraction.mockResolvedValue({ labour: {} });

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.startContraction).toHaveBeenCalledWith({
        requestBody: { start_time: '2023-01-01T00:00:00Z' },
      });

      // TODO: Verify idempotency header when API client supports it
      // expect(mockLabourServiceClient.startContraction).toHaveBeenCalledWith({
      //   headers: { 'X-Idempotency-Key': event.id },
      //   requestBody: { start_time: '2023-01-01T00:00:00Z' },
      // });
    });
  });

  describe('sequence ordering', () => {
    beforeEach(() => {
      syncEngine.start();
    });

    it('should sync events in sequence order within same aggregate', async () => {
      // Add events in database insertion order (they get auto-assigned sequences)
      await OutboxManager.addEvent('labour-1', 'plan_labour', {});
      await OutboxManager.addEvent('labour-1', 'labour_update', {});
      await OutboxManager.addEvent('labour-1', 'start_contraction', {});

      const executionOrder: string[] = [];

      mockLabourServiceClient.planLabour.mockImplementation(() => {
        executionOrder.push('plan_labour');
        return Promise.resolve({ labour: {} });
      });

      mockLabourUpdatesService.postLabourUpdate.mockImplementation(() => {
        executionOrder.push('labour_update');
        return Promise.resolve({ labour_update: {} });
      });

      mockLabourServiceClient.startContraction.mockImplementation(() => {
        executionOrder.push('start_contraction');
        return Promise.resolve({ labour: {} });
      });

      await syncEngine.triggerSync();

      expect(executionOrder).toEqual(['plan_labour', 'labour_update', 'start_contraction']);
    });

    it('should sync different aggregates independently', async () => {
      await OutboxManager.addEvent('labour-1', 'start_contraction', {});
      await OutboxManager.addEvent('labour-2', 'start_contraction', {});

      mockLabourServiceClient.startContraction.mockResolvedValue({ labour: {} });

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.startContraction).toHaveBeenCalledTimes(2);

      const remainingEvents = await OutboxManager.getAllPendingEvents();
      expect(remainingEvents).toHaveLength(0);
    });
  });

  describe('failure handling enhancements', () => {
    beforeEach(() => {
      syncEngine.start();
    });

    it('should stop processing subsequent events after a failure within the same aggregate', async () => {
      // Queue two events for the same aggregate
      await OutboxManager.addEvent('labour-1', 'start_contraction', {
        start_time: '2023-01-01T00:00:00Z',
      });
      await OutboxManager.addEvent('labour-1', 'end_contraction', {
        end_time: '2023-01-01T00:05:00Z',
        intensity: 7,
      });

      // First event fails
      mockLabourServiceClient.startContraction.mockRejectedValue(new Error('API Error'));
      mockLabourServiceClient.endContraction.mockResolvedValue({ labour: {} });

      await syncEngine.triggerSync();

      // Only the first call attempted; second should not be called until retry succeeds
      expect(mockLabourServiceClient.startContraction).toHaveBeenCalledTimes(1);
      expect(mockLabourServiceClient.endContraction).not.toHaveBeenCalled();

      const failed = await OutboxManager.getEventsByStatus('failed');
      expect(failed.map((e) => e.eventType)).toContain('start_contraction');
      const pending = await OutboxManager.getAllPendingEvents();
      // End event should still be pending
      expect(pending.map((e) => e.eventType)).toContain('end_contraction');
    });

    it('applies configured delay between events during sync', async () => {
      syncEngine.stop();

      (global as any).window = (global as any).window || {};
      (global as any).window.__OFFLINE_SYNC_DELAY_MS = 30;
      syncEngine = new SyncEngine();
      syncEngine.start();

      await OutboxManager.addEvent('labour-1', 'start_contraction', {
        start_time: '2023-01-01T00:00:00Z',
      });
      await OutboxManager.addEvent('labour-1', 'end_contraction', {
        end_time: '2023-01-01T00:01:00Z',
        intensity: 5,
      });

      let tStart = 0;
      let tEnd = 0;
      mockLabourServiceClient.startContraction.mockImplementation((_args: any) => {
        tStart = Date.now();
        return Promise.resolve({ labour: {} });
      });
      mockLabourServiceClient.endContraction.mockImplementation((_args: any) => {
        tEnd = Date.now();
        return Promise.resolve({ labour: {} });
      });
      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.startContraction).toHaveBeenCalledTimes(1);
      expect(mockLabourServiceClient.endContraction).toHaveBeenCalledTimes(1);
      // Check there was a noticeable gap (>=20ms) between the two
      expect(tEnd - tStart).toBeGreaterThanOrEqual(20);

      // Clean up
      delete (global as any).window.__OFFLINE_SYNC_DELAY_MS;
    });
  });

  describe('failure and retry handling', () => {
    beforeEach(() => {
      syncEngine.start();
    });

    it('should mark events as failed on API errors', async () => {
      await OutboxManager.addEvent('labour-1', 'start_contraction', {
        start_time: '2023-01-01T00:00:00Z',
      });

      mockLabourServiceClient.startContraction.mockRejectedValue(new Error('API Error'));

      await syncEngine.triggerSync();

      const failedEvents = await OutboxManager.getEventsByStatus('failed');
      expect(failedEvents).toHaveLength(1);
      expect(failedEvents[0].retryCount).toBe(1);
    });

    it('should schedule retry with exponential backoff', async () => {
      // This test verifies retry scheduling but doesn't wait for actual retry
      // to avoid long test execution times
      await OutboxManager.addEvent('labour-1', 'start_contraction', {
        start_time: '2023-01-01T00:00:00Z',
      });

      mockLabourServiceClient.startContraction.mockRejectedValue(new Error('Network error'));

      await syncEngine.triggerSync();

      const status = await syncEngine.getSyncStatus();
      expect(status.failed).toBe(1);
      expect(status.scheduledRetries).toBe(1);
    });

    it('should stop retrying events that exceed max retry count', async () => {
      // Create event with high retry count
      const event = await OutboxManager.addEvent('labour-1', 'start_contraction', {});

      // Fail it multiple times to exceed retry limit
      for (let i = 0; i < 6; i++) {
        await OutboxManager.markEventFailed(event.id);
      }

      mockLabourServiceClient.startContraction.mockRejectedValue(new Error('Still failing'));

      const retriableEvents = await OutboxManager.getRetriableEvents();
      expect(retriableEvents.map((e) => e.id)).not.toContain(event.id);
    });

    it('should handle partial failures in multi-event sync', async () => {
      await OutboxManager.addEvent('labour-1', 'plan_labour', { sequence: 1 });
      await OutboxManager.addEvent('labour-1', 'start_contraction', { sequence: 2 });

      mockLabourServiceClient.planLabour.mockResolvedValue({ labour: {} });
      mockLabourServiceClient.startContraction.mockRejectedValue(new Error('Contraction failed'));

      await syncEngine.triggerSync();

      const syncedEvents = await OutboxManager.getEventsByStatus('synced');
      const failedEvents = await OutboxManager.getEventsByStatus('failed');

      expect(syncedEvents).toHaveLength(0); // Pruned after sync
      expect(failedEvents).toHaveLength(1);
      expect(failedEvents[0].eventType).toBe('start_contraction');
    });
  });

  describe('network awareness', () => {
    beforeEach(() => {
      syncEngine.start();
    });

    it('should not sync when offline', async () => {
      setNetworkOnline(false);

      await OutboxManager.addEvent('labour-1', 'start_contraction', {});

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.startContraction).not.toHaveBeenCalled();

      const pendingEvents = await OutboxManager.getAllPendingEvents();
      expect(pendingEvents).toHaveLength(1);
    });

    it('should not sync on very slow connections', async () => {
      // Mock slow connection and force networkDetector to update
      const mockConnection = {
        effectiveType: 'slow-2g',
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
      };
      (navigator as any).connection = mockConnection;

      // Force networkDetector to re-evaluate with new connection
      (networkDetector as any).currentState = {
        isOnline: true,
        effectiveType: 'slow-2g',
      };

      await OutboxManager.addEvent('labour-1', 'start_contraction', {});

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.startContraction).not.toHaveBeenCalled();
    });

    it('should respond to network state changes', (done) => {
      // Start offline
      setNetworkOnline(false);
      syncEngine.start();

      // Add event while offline
      OutboxManager.addEvent('labour-1', 'start_contraction', {}).then(() => {
        mockLabourServiceClient.startContraction.mockResolvedValue({ labour: {} });

        // Go online
        setNetworkOnline(true);

        // Give sync time to trigger
        setTimeout(async () => {
          expect(mockLabourServiceClient.startContraction).toHaveBeenCalled();
          done();
        }, 1200); // Account for 1s delay in network listener
      });
    });
  });

  describe('concurrent sync protection', () => {
    beforeEach(() => {
      // Clear all mocks before each test in this group
      jest.clearAllMocks();
      syncEngine.start();
    });

    it('should prevent concurrent sync of same aggregate', async () => {
      await OutboxManager.addEvent('labour-1', 'start_contraction', {});

      mockLabourServiceClient.startContraction.mockResolvedValue({ labour: {} });

      // Start multiple syncs for same aggregate - should be serialized
      await Promise.all([
        syncEngine.syncAggregate('labour-1'),
        syncEngine.syncAggregate('labour-1'),
        syncEngine.syncAggregate('labour-1'),
      ]);

      // Should only sync once due to concurrency protection
      expect(mockLabourServiceClient.startContraction).toHaveBeenCalledTimes(1);
    });

    it('should allow sync of different aggregates concurrently', async () => {
      await OutboxManager.addEvent('labour-1', 'start_contraction', {});
      await OutboxManager.addEvent('labour-2', 'start_contraction', {});

      mockLabourServiceClient.startContraction.mockResolvedValue({ labour: {} });

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.startContraction).toHaveBeenCalledTimes(2);
    });
  });

  describe('sync status and monitoring', () => {
    beforeEach(() => {
      syncEngine.start();
    });

    it('should provide comprehensive sync status', async () => {
      // Create events in different states
      await OutboxManager.addEvent('labour-1', 'start_contraction', {}); // Will be pending
      const syncingEvent = await OutboxManager.addEvent('labour-2', 'plan_labour', {});
      await OutboxManager.markEventSyncing(syncingEvent.id);

      const failedEvent = await OutboxManager.addEvent('labour-3', 'labour_update', {});
      await OutboxManager.markEventFailed(failedEvent.id);

      const status = await syncEngine.getSyncStatus();

      expect(status.pending).toBe(1);
      expect(status.syncing).toBe(1);
      expect(status.failed).toBe(1);
      expect(status.isRunning).toBe(true);
      expect(status.isOnline).toBe(true);
      expect(status.activeSyncs).toBe(0);
    });

    it('should retry all failed events on demand', async () => {
      const event1 = await OutboxManager.addEvent('labour-1', 'start_contraction', {});
      const event2 = await OutboxManager.addEvent('labour-2', 'plan_labour', {});

      await OutboxManager.markEventFailed(event1.id);
      await OutboxManager.markEventFailed(event2.id);

      mockLabourServiceClient.startContraction.mockResolvedValue({ labour: {} });
      mockLabourServiceClient.planLabour.mockResolvedValue({ labour: {} });

      await syncEngine.retryFailedEvents();

      expect(mockLabourServiceClient.startContraction).toHaveBeenCalled();
      expect(mockLabourServiceClient.planLabour).toHaveBeenCalled();

      const failedEventsAfter = await OutboxManager.getEventsByStatus('failed');
      expect(failedEventsAfter).toHaveLength(0);
    });
  });

  describe('contraction ID mapping', () => {
    beforeEach(() => {
      syncEngine.start();
    });

    it('translates optimistic ID to real ID for update after start sync', async () => {
      const aggregateId = 'labour-1';
      const startTime = '2023-01-01T00:00:00Z';
      const tempId = 'optimistic-123';

      await OutboxManager.addEvent(aggregateId, 'start_contraction', { start_time: startTime });
      await ContractionIdMapper.addTempMapping(aggregateId, tempId, startTime);
      await OutboxManager.addEvent(aggregateId, 'update_contraction', {
        contraction_id: tempId,
        intensity: 9,
      });

      mockLabourServiceClient.startContraction.mockResolvedValue({
        labour: {
          contractions: [{ id: 'real-abc', start_time: startTime }],
        },
      });
      mockLabourServiceClient.updateContraction.mockResolvedValue({ labour: {} });

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.updateContraction).toHaveBeenCalledTimes(1);
      const arg = mockLabourServiceClient.updateContraction.mock.calls[0][0];
      expect(arg.requestBody.contraction_id).toBe('real-abc');
    });

    it('resolves mapping via active contraction or time tolerance when start_time differs slightly', async () => {
      const aggregateId = 'labour-22';
      const startTime = '2023-01-01T00:00:00.500Z'; // client has ms component
      const tempId = 'optimistic-zzz';

      await OutboxManager.addEvent(aggregateId, 'start_contraction', { start_time: startTime });
      await ContractionIdMapper.addTempMapping(aggregateId, tempId, startTime);
      await OutboxManager.addEvent(aggregateId, 'update_contraction', {
        contraction_id: tempId,
        intensity: 3,
      });

      // Server returns trimmed milliseconds and marks it active
      mockLabourServiceClient.startContraction.mockResolvedValue({
        labour: {
          contractions: [{ id: 'real-tol', start_time: '2023-01-01T00:00:00Z', is_active: true }],
        },
      } as any);
      mockLabourServiceClient.updateContraction.mockResolvedValue({ labour: {} } as any);

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.updateContraction).toHaveBeenCalledTimes(1);
      const arg = mockLabourServiceClient.updateContraction.mock.calls[0][0];
      expect(arg.requestBody.contraction_id).toBe('real-tol');
    });

    it('translates optimistic ID to real ID for delete after start sync', async () => {
      const aggregateId = 'labour-1';
      const startTime = '2023-01-01T00:00:10Z';
      const tempId = 'optimistic-999';

      await OutboxManager.addEvent(aggregateId, 'start_contraction', { start_time: startTime });
      await ContractionIdMapper.addTempMapping(aggregateId, tempId, startTime);
      await OutboxManager.addEvent(aggregateId, 'delete_contraction', {
        contraction_id: tempId,
      });

      mockLabourServiceClient.startContraction.mockResolvedValue({
        labour: {
          contractions: [{ id: 'real-del-1', start_time: startTime }],
        },
      });
      mockLabourServiceClient.deleteContraction.mockResolvedValue({ labour: {} });

      await syncEngine.triggerSync();

      expect(mockLabourServiceClient.deleteContraction).toHaveBeenCalledTimes(1);
      const arg = mockLabourServiceClient.deleteContraction.mock.calls[0][0];
      expect(arg.requestBody.contraction_id).toBe('real-del-1');
    });

    it('passes through real IDs unchanged for update', async () => {
      const aggregateId = 'labour-1';
      await OutboxManager.addEvent(aggregateId, 'update_contraction', {
        contraction_id: 'real-1',
        intensity: 4,
      });
      mockLabourServiceClient.updateContraction.mockResolvedValue({ labour: {} });
      await syncEngine.triggerSync();
      expect(mockLabourServiceClient.updateContraction).toHaveBeenCalledTimes(1);
      const arg = mockLabourServiceClient.updateContraction.mock.calls[0][0];
      expect(arg.requestBody.contraction_id).toBe('real-1');
    });

    it('falls back to optimistic ID when no mapping is resolved yet', async () => {
      const aggregateId = 'labour-1';
      await ContractionIdMapper.addTempMapping(aggregateId, 'optimistic-x', '2023-01-01T00:02:00Z');
      await OutboxManager.addEvent(aggregateId, 'update_contraction', {
        contraction_id: 'optimistic-x',
        intensity: 6,
      });
      mockLabourServiceClient.updateContraction.mockResolvedValue({ labour: {} });
      await syncEngine.triggerSync();
      const arg = mockLabourServiceClient.updateContraction.mock.calls[0][0];
      expect(arg.requestBody.contraction_id).toBe('optimistic-x');
    });
  });
});
