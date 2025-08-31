import { generateEventId } from '../utils/eventId';
import { offlineLogger } from '../utils/logger';
import { SequenceManager } from '../utils/sequenceManager';
import { db, OutboxEvent } from './database';

export type OutboxEventStatus = 'pending' | 'syncing' | 'synced' | 'failed';
export type EventType =
  | 'plan_labour'
  | 'start_contraction'
  | 'end_contraction'
  | 'complete_labour'
  | 'labour_update'
  | 'delete_contraction'
  | 'update_contraction';

/**
 * Outbox management for offline-first event sourcing
 * Handles event queueing, ordering, and auto-pruning
 */
export class OutboxManager {
  /**
   * Add a new event to the outbox
   */
  static async addEvent(
    aggregateId: string,
    eventType: EventType,
    payload: unknown,
    isGuestEvent: boolean = false
  ): Promise<OutboxEvent> {
    const eventId = generateEventId();
    const sequence = await SequenceManager.getNextSequence(aggregateId);

    const event: OutboxEvent = {
      id: eventId,
      aggregateId,
      aggregateType: 'labour',
      eventType,
      sequence,
      payload,
      status: 'pending',
      createdAt: new Date(),
      retryCount: 0,
      isGuestEvent: isGuestEvent ? 1 : 0,
    };

    await db.outbox.add(event);
    offlineLogger.debug('outbox:add', {
      aggregateId,
      eventType,
      sequence,
      isGuestEvent,
      id: eventId,
    });
    return event;
  }

  /**
   * Get all pending events for an aggregate in sequence order
   */
  static async getPendingEvents(aggregateId: string): Promise<OutboxEvent[]> {
    const events = await db.outbox.where({ aggregateId, status: 'pending' }).sortBy('sequence');
    offlineLogger.debug('outbox:pending', { aggregateId, count: events.length });
    return events;
  }

  /**
   * Get all pending events across all aggregates
   */
  static async getAllPendingEvents(): Promise<OutboxEvent[]> {
    const events = await db.outbox.where('status').equals('pending').sortBy('createdAt');
    offlineLogger.debug('outbox:pendingAll', { count: events.length });
    return events;
  }

  /**
   * Mark an event as syncing
   */
  static async markEventSyncing(eventId: string): Promise<void> {
    await db.outbox.update(eventId, { status: 'syncing' });
    offlineLogger.debug('outbox:status', { eventId, status: 'syncing' });
  }

  /**
   * Mark an event as successfully synced and prune if not guest event
   */
  static async markEventSynced(eventId: string): Promise<void> {
    const event = await db.outbox.get(eventId);
    if (!event) {
      return;
    }

    await db.outbox.update(eventId, { status: 'synced' });

    if (!event.isGuestEvent) {
      await db.outbox.delete(eventId);
    }
    offlineLogger.debug('outbox:status', {
      eventId,
      status: 'synced',
      pruned: !event.isGuestEvent,
    });
  }

  /**
   * Mark an event as failed and increment retry count
   */
  static async markEventFailed(eventId: string, error?: string): Promise<void> {
    const event = await db.outbox.get(eventId);
    if (!event) {
      return;
    }

    await db.outbox.update(eventId, {
      status: 'failed',
      retryCount: event.retryCount + 1,
    });
    offlineLogger.warn('outbox:status', {
      eventId,
      status: 'failed',
      retryCount: event.retryCount + 1,
      error,
    });
  }

  /**
   * Reset failed event back to pending for retry
   */
  static async retryEvent(eventId: string): Promise<void> {
    await db.outbox.update(eventId, { status: 'pending' });
    offlineLogger.info('outbox:status', { eventId, status: 'pending' });
  }

  /**
   * Get failed events that should be retried
   */
  static async getRetriableEvents(maxRetries: number = 5): Promise<OutboxEvent[]> {
    return await db.outbox
      .where('status')
      .equals('failed')
      .and((event) => event.retryCount < maxRetries)
      .toArray();
  }

  /**
   * Get events by status
   */
  static async getEventsByStatus(status: OutboxEventStatus): Promise<OutboxEvent[]> {
    const events = await db.outbox.where('status').equals(status).sortBy('createdAt');
    offlineLogger.debug('outbox:byStatus', { status, count: events.length });
    return events;
  }

  /**
   * Delete specific event (for manual cleanup)
   */
  static async deleteEvent(eventId: string): Promise<void> {
    await db.outbox.delete(eventId);
    offlineLogger.info('outbox:delete', { eventId });
  }

  /**
   * Manually prune synced non-guest events
   * Called periodically for maintenance
   */
  static async pruneSyncedEvents(): Promise<number> {
    const syncedEvents = await db.outbox
      .where('status')
      .equals('synced')
      .and((event) => !event.isGuestEvent)
      .toArray();

    const eventIds = syncedEvents.map((e) => e.id);
    await db.outbox.bulkDelete(eventIds);

    offlineLogger.info('outbox:prune', { count: eventIds.length });
    return eventIds.length;
  }

  /**
   * Get guest events for migration during upgrade
   */
  static async getGuestEvents(): Promise<OutboxEvent[]> {
    // Simpler query for broad compatibility with test environments
    const events = await db.outbox.where('isGuestEvent').equals(1).sortBy('sequence');
    offlineLogger.debug('outbox:guestEvents', { count: events.length });
    return events;
  }

  /**
   * Mark guest events as upgraded after migration
   */
  static async markGuestEventsUpgraded(eventIds: string[]): Promise<void> {
    await db.outbox.bulkUpdate(eventIds.map((id) => ({ key: id, changes: { isGuestEvent: 0 } })));
    offlineLogger.info('outbox:upgradeGuest', { count: eventIds.length });
  }

  /**
   * Get outbox statistics for monitoring
   */
  static async getStats() {
    const [pending, syncing, synced, failed, guest] = await Promise.all([
      db.outbox.where('status').equals('pending').count(),
      db.outbox.where('status').equals('syncing').count(),
      db.outbox.where('status').equals('synced').count(),
      db.outbox.where('status').equals('failed').count(),
      db.outbox.where('isGuestEvent').equals(1).count(),
    ]);

    const stats = { pending, syncing, synced, failed, guest };
    if (hasOutboxStatsChanged(stats)) {
      offlineLogger.debug('outbox:stats', stats);
      setLastOutboxStats(stats);
    }
    return stats;
  }

  /**
   * Clear all events (for testing/reset)
   */
  static async clearAll(): Promise<void> {
    await db.outbox.clear();
  }
}

// Track last emitted outbox stats to avoid duplicate logs
let __lastOutboxStats: {
  pending: number;
  syncing: number;
  synced: number;
  failed: number;
  guest: number;
} | null = null;

function hasOutboxStatsChanged(current: {
  pending: number;
  syncing: number;
  synced: number;
  failed: number;
  guest: number;
}) {
  const last = __lastOutboxStats;
  if (!last) {
    return true;
  }
  return (
    last.pending !== current.pending ||
    last.syncing !== current.syncing ||
    last.synced !== current.synced ||
    last.failed !== current.failed ||
    last.guest !== current.guest
  );
}

function setLastOutboxStats(current: {
  pending: number;
  syncing: number;
  synced: number;
  failed: number;
  guest: number;
}) {
  __lastOutboxStats = current;
}
