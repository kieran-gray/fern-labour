import Dexie, { Table } from 'dexie';
import type { ContractionIdMap } from './contractionIdMap';

export interface OutboxEvent {
  id: string;
  aggregateId: string;
  aggregateType: 'labour';
  eventType:
    | 'plan_labour'
    | 'start_contraction'
    | 'end_contraction'
    | 'complete_labour'
    | 'labour_update'
    | 'delete_contraction'
    | 'update_contraction';
  sequence: number;
  payload: unknown;
  status: 'pending' | 'syncing' | 'synced' | 'failed';
  createdAt: Date;
  retryCount: number;
  isGuestEvent: 0 | 1;
}

export interface SequenceCounter {
  aggregateId: string;
  sequence: number;
}

export class OfflineDatabase extends Dexie {
  outbox!: Table<OutboxEvent>;
  sequences!: Table<SequenceCounter>;
  contractionIdMap!: Table<ContractionIdMap>;

  constructor() {
    super('FernLabourOfflineDB');

    this.version(1).stores({
      outbox: `
        id,
        aggregateId,
        aggregateType,
        eventType,
        sequence,
        status,
        createdAt,
        isGuestEvent,
        retryCount,
        [isGuestEvent+aggregateId+sequence],
        [aggregateId+status]
      `,
      sequences: 'aggregateId, sequence',
      contractionIdMap: `
        tempId,
        aggregateId,
        startTime,
        realId,
        createdAt,
        [aggregateId+startTime]
      `,
    });
  }
}

export const db = new OfflineDatabase();

export async function initializeDatabase(): Promise<void> {
  await db.open();
}

export async function clearAllData(): Promise<void> {
  await db.transaction('rw', [db.outbox, db.sequences], async () => {
    await db.outbox.clear();
    await db.sequences.clear();
  });
}

export async function getDatabaseStats() {
  const [outboxCount, sequenceCount] = await Promise.all([db.outbox.count(), db.sequences.count()]);

  return {
    outboxEvents: outboxCount,
    sequences: sequenceCount,
    storage: (await navigator.storage?.estimate?.()) || { usage: 0, quota: 0 },
  };
}
