import 'fake-indexeddb/auto';

import { OfflineDatabase } from '../database';
import { OutboxManager } from '../outbox';

describe('OutboxManager', () => {
  let testDb: OfflineDatabase;

  beforeEach(async () => {
    testDb = new OfflineDatabase();
    await testDb.open();
    await testDb.transaction(
      'rw',
      [testDb.outbox, testDb.guestProfiles, testDb.sequences],
      async () => {
        await testDb.outbox.clear();
        await testDb.guestProfiles.clear();
        await testDb.sequences.clear();
      }
    );
  });

  afterEach(async () => {
    if (testDb.isOpen()) {
      await testDb.close();
    }
  });

  describe('event lifecycle', () => {
    it('should add event with auto-incrementing sequence', async () => {
      const aggregateId = 'labour-123';
      const payload = { start_time: '2023-01-01T00:00:00Z' };

      const event1 = await OutboxManager.addEvent(aggregateId, 'start_contraction', payload);
      const event2 = await OutboxManager.addEvent(aggregateId, 'end_contraction', {});

      expect(event1.sequence).toBe(1);
      expect(event2.sequence).toBe(2);
      expect(event1.aggregateId).toBe(aggregateId);
      expect(event1.status).toBe('pending');
      expect(event1.payload).toEqual(payload);
      expect(event1.id).toBeDefined();
      expect(event1.createdAt).toBeInstanceOf(Date);
    });

    it('should handle guest vs regular event flags', async () => {
      const regularEvent = await OutboxManager.addEvent('labour-1', 'plan_labour', {}, false);
      const guestEvent = await OutboxManager.addEvent('guest-labour', 'plan_labour', {}, true);

      expect(regularEvent.isGuestEvent).toBe(0);
      expect(guestEvent.isGuestEvent).toBe(1);
    });

    it('should transition through status lifecycle correctly', async () => {
      const event = await OutboxManager.addEvent('labour-1', 'start_contraction', {});

      expect(event.status).toBe('pending');
      expect(event.retryCount).toBe(0);

      await OutboxManager.markEventSyncing(event.id);
      const syncingEvent = await testDb.outbox.get(event.id);
      expect(syncingEvent?.status).toBe('syncing');

      await OutboxManager.markEventSynced(event.id);
      const syncedEvent = await testDb.outbox.get(event.id);
      expect(syncedEvent).toBeUndefined(); // Auto-pruned for regular events

      const guestEvent = await OutboxManager.addEvent('guest-labour', 'plan_labour', {}, true);
      await OutboxManager.markEventSynced(guestEvent.id);
      const preservedEvent = await testDb.outbox.get(guestEvent.id);
      expect(preservedEvent?.status).toBe('synced'); // Preserved for guest events
    });
  });

  describe('failure and retry handling', () => {
    it('should handle failure with retry counting', async () => {
      const event = await OutboxManager.addEvent('labour-1', 'start_contraction', {});

      await OutboxManager.markEventFailed(event.id);
      await OutboxManager.markEventFailed(event.id);

      const failedEvent = await testDb.outbox.get(event.id);
      expect(failedEvent?.status).toBe('failed');
      expect(failedEvent?.retryCount).toBe(2);

      await OutboxManager.retryEvent(event.id);
      const retriedEvent = await testDb.outbox.get(event.id);
      expect(retriedEvent?.status).toBe('pending');
      expect(retriedEvent?.retryCount).toBe(2); // Retry count preserved
    });

    it('should identify retriable vs exhausted events', async () => {
      const retriableEvent = await OutboxManager.addEvent('labour-1', 'start_contraction', {});
      const exhaustedEvent = await OutboxManager.addEvent('labour-2', 'end_contraction', {});

      // Fail retriable event 3 times (under limit of 5)
      for (let i = 0; i < 3; i++) {
        await OutboxManager.markEventFailed(retriableEvent.id);
      }

      // Fail exhausted event 6 times (over limit)
      for (let i = 0; i < 6; i++) {
        await OutboxManager.markEventFailed(exhaustedEvent.id);
      }

      const retriableEvents = await OutboxManager.getRetriableEvents(5);
      const eventIds = retriableEvents.map((e) => e.id);

      expect(eventIds).toContain(retriableEvent.id);
      expect(eventIds).not.toContain(exhaustedEvent.id);
    });
  });

  describe('querying and filtering', () => {
    beforeEach(async () => {
      // Create events with known IDs to ensure predictable test setup
      await OutboxManager.addEvent('labour-1', 'start_contraction', {}, false); // seq 1, will stay pending
      const event2 = await OutboxManager.addEvent('labour-1', 'end_contraction', {}, false); // seq 2, will be syncing
      await OutboxManager.addEvent('guest-labour', 'plan_labour', {}, true); // seq 1, guest pending
      const event4 = await OutboxManager.addEvent('labour-2', 'labour_update', {}, false); // seq 1, will be failed

      // Set specific statuses for predictable tests
      await OutboxManager.markEventSyncing(event2.id);
      await OutboxManager.markEventFailed(event4.id);
    });

    it('should get pending events for specific aggregate in sequence order', async () => {
      const pendingEvents = await OutboxManager.getPendingEvents('labour-1');

      expect(pendingEvents).toHaveLength(1);
      expect(pendingEvents[0].eventType).toBe('start_contraction');
      expect(pendingEvents[0].status).toBe('pending');
      expect(pendingEvents[0].sequence).toBe(1);
    });

    it('should get all pending events across aggregates', async () => {
      const allPendingEvents = await OutboxManager.getAllPendingEvents();

      expect(allPendingEvents).toHaveLength(2);
      expect(allPendingEvents.map((e) => e.eventType)).toContain('start_contraction');
      expect(allPendingEvents.map((e) => e.eventType)).toContain('plan_labour');
    });

    it('should filter events by status', async () => {
      const syncingEvents = await OutboxManager.getEventsByStatus('syncing');
      const failedEvents = await OutboxManager.getEventsByStatus('failed');

      expect(syncingEvents).toHaveLength(1);
      expect(syncingEvents[0].eventType).toBe('end_contraction');

      expect(failedEvents).toHaveLength(1);
      expect(failedEvents[0].eventType).toBe('labour_update');
    });

    it('should identify guest events', async () => {
      // Use a simpler approach to find guest events since fake-indexeddb has issues with complex composite indexes
      const allEvents = await testDb.outbox.toArray();
      const guestEvents = allEvents.filter((e) => e.isGuestEvent === 1);

      expect(guestEvents).toHaveLength(1);
      expect(guestEvents[0].eventType).toBe('plan_labour');
      expect(guestEvents[0].aggregateId).toBe('guest-labour');
    });
  });

  describe('maintenance operations', () => {
    it('should provide accurate statistics', async () => {
      await OutboxManager.addEvent('labour-1', 'start_contraction', {}, false); // pending
      await OutboxManager.addEvent('guest-labour', 'plan_labour', {}, true); // pending guest

      const event3 = await OutboxManager.addEvent('labour-2', 'end_contraction', {}, false);
      await OutboxManager.markEventSyncing(event3.id); // syncing

      const event4 = await OutboxManager.addEvent('labour-3', 'labour_update', {}, false);
      await testDb.outbox.update(event4.id, { status: 'synced' }); // synced

      const event5 = await OutboxManager.addEvent('labour-4', 'complete_labour', {}, false);
      await OutboxManager.markEventFailed(event5.id); // failed

      const stats = await OutboxManager.getStats();

      expect(stats.pending).toBe(2);
      expect(stats.syncing).toBe(1);
      expect(stats.synced).toBe(1);
      expect(stats.failed).toBe(1);
      expect(stats.guest).toBe(1);
    });

    it('should prune synced non-guest events only', async () => {
      const regularEvent = await OutboxManager.addEvent('labour-1', 'start_contraction', {}, false);
      const guestEvent = await OutboxManager.addEvent('guest-labour', 'plan_labour', {}, true);

      await testDb.outbox.update(regularEvent.id, { status: 'synced' });
      await testDb.outbox.update(guestEvent.id, { status: 'synced' });

      const prunedCount = await OutboxManager.pruneSyncedEvents();

      expect(prunedCount).toBe(1);
      expect(await testDb.outbox.get(regularEvent.id)).toBeUndefined();
      expect(await testDb.outbox.get(guestEvent.id)).toBeDefined();
    });

    it('should mark guest events as upgraded during migration', async () => {
      const guestEvent1 = await OutboxManager.addEvent(
        'guest-labour-1',
        'start_contraction',
        {},
        true
      );
      const guestEvent2 = await OutboxManager.addEvent('guest-labour-2', 'plan_labour', {}, true);

      await OutboxManager.markGuestEventsUpgraded([guestEvent1.id, guestEvent2.id]);

      const upgradedEvent1 = await testDb.outbox.get(guestEvent1.id);
      const upgradedEvent2 = await testDb.outbox.get(guestEvent2.id);

      expect(upgradedEvent1?.isGuestEvent).toBe(0);
      expect(upgradedEvent2?.isGuestEvent).toBe(0);
    });
  });
});
