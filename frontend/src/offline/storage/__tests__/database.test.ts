import 'fake-indexeddb/auto';

import { OfflineDatabase, OutboxEvent } from '../database';

describe('OfflineDatabase', () => {
  let db: OfflineDatabase;

  beforeEach(async () => {
    db = new OfflineDatabase();
    await db.open();

    await db.transaction('rw', [db.outbox, db.guestProfiles, db.sequences], async () => {
      await db.outbox.clear();
      await db.guestProfiles.clear();
      await db.sequences.clear();
    });
  });

  afterEach(async () => {
    if (db.isOpen()) {
      await db.close();
    }
  });

  describe('schema validation', () => {
    it('should have all required tables', () => {
      const tableNames = db.tables.map((t) => t.name).sort();
      expect(tableNames).toEqual(['contractionIdMap', 'guestProfiles', 'outbox', 'sequences']);
    });

    it('should have composite index for event ordering', () => {
      const outboxTable = db.outbox;
      const hasCompositeIndex = outboxTable.schema.indexes.some(
        (index) => index.name === '[isGuestEvent+aggregateId+sequence]'
      );
      expect(hasCompositeIndex).toBe(true);
    });
  });

  describe('atomic operations', () => {
    it('should handle cross-table transactions', async () => {
      await db.transaction('rw', [db.outbox, db.guestProfiles, db.sequences], async () => {
        await db.outbox.add({
          id: 'event-1',
          aggregateId: 'labour-123',
          aggregateType: 'labour',
          eventType: 'plan_labour',
          sequence: 1,
          payload: {},
          status: 'pending',
          createdAt: new Date(),
          retryCount: 0,
          isGuestEvent: 1,
        });

        await db.guestProfiles.add({
          guestId: 'guest-123',
          createdAt: new Date(),
          labours: [],
          isUpgraded: 0,
          lastActiveAt: new Date(),
        });

        await db.sequences.add({
          aggregateId: 'labour-123',
          sequence: 1,
        });
      });

      const [eventCount, profileCount, seqCount] = await Promise.all([
        db.outbox.count(),
        db.guestProfiles.count(),
        db.sequences.count(),
      ]);

      expect(eventCount).toBe(1);
      expect(profileCount).toBe(1);
      expect(seqCount).toBe(1);
    });
  });

  describe('query patterns', () => {
    beforeEach(async () => {
      const events: OutboxEvent[] = [
        {
          id: 'guest-event-1',
          aggregateId: 'guest-labour',
          aggregateType: 'labour',
          eventType: 'plan_labour',
          sequence: 1,
          payload: {},
          status: 'pending',
          createdAt: new Date(),
          retryCount: 0,
          isGuestEvent: 1,
        },
        {
          id: 'guest-event-2',
          aggregateId: 'guest-labour',
          aggregateType: 'labour',
          eventType: 'start_contraction',
          sequence: 2,
          payload: {},
          status: 'synced',
          createdAt: new Date(),
          retryCount: 0,
          isGuestEvent: 1,
        },
        {
          id: 'user-event-1',
          aggregateId: 'user-labour',
          aggregateType: 'labour',
          eventType: 'plan_labour',
          sequence: 1,
          payload: {},
          status: 'failed',
          createdAt: new Date(),
          retryCount: 3,
          isGuestEvent: 0,
        },
      ];

      await db.outbox.bulkAdd(events);
    });

    it('should find pending guest events in sequence order', async () => {
      const pendingGuestEvents = await db.outbox
        .where('[isGuestEvent+aggregateId]')
        .equals([1, 'guest-labour'])
        .and((event) => event.status === 'pending')
        .sortBy('sequence');

      expect(pendingGuestEvents).toHaveLength(1);
      expect(pendingGuestEvents[0].id).toBe('guest-event-1');
      expect(pendingGuestEvents[0].sequence).toBe(1);
    });

    it('should find events by exact composite key', async () => {
      const specificEvent = await db.outbox
        .where('[isGuestEvent+aggregateId+sequence]')
        .equals([1, 'guest-labour', 2])
        .first();

      expect(specificEvent?.id).toBe('guest-event-2');
      expect(specificEvent?.eventType).toBe('start_contraction');
    });

    it('should find failed events needing retry', async () => {
      const failedEvents = await db.outbox
        .where('status')
        .equals('failed')
        .and((event) => event.retryCount < 5)
        .toArray();

      expect(failedEvents).toHaveLength(1);
      expect(failedEvents[0].id).toBe('user-event-1');
    });
  });
});
