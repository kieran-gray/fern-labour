import { db } from './database';

/**
 * Mapping between client-side optimistic contraction IDs and real server IDs.
 * Keyed by `tempId` per aggregate. Also carries the start time used when creating
 * the contraction so we can resolve the mapping after the start event sync returns.
 */
export interface ContractionIdMap {
  tempId: string;
  aggregateId: string;
  startTime: string;
  realId: string | null;
  createdAt: Date;
}

export class ContractionIdMapper {
  /**
   * Record a new temporary mapping for an optimistic contraction.
   */
  static async addTempMapping(
    aggregateId: string,
    tempId: string,
    startTime: string
  ): Promise<void> {
    try {
      await db.contractionIdMap.put({
        tempId,
        aggregateId,
        startTime,
        realId: null,
        createdAt: new Date(),
      });
    } catch {
      // no-op
    }
  }

  /**
   * Resolve a mapping by start time once the real contraction ID is known.
   */
  static async resolveByStartTime(
    aggregateId: string,
    startTime: string,
    realId: string
  ): Promise<void> {
    const candidates = await db.contractionIdMap
      .where('[aggregateId+startTime]')
      .equals([aggregateId, startTime])
      .toArray();
    if (candidates.length === 0) {
      return;
    }

    // Update all candidates that don't yet have a realId
    const updates = candidates
      .filter((c) => !c.realId)
      .map((c) => ({ key: c.tempId, changes: { realId } }));
    if (updates.length > 0) {
      await db.contractionIdMap.bulkUpdate(updates);
    }
  }

  /**
   * Return the real ID if the provided ID is a known temporary one for this aggregate.
   * Falls back to the provided ID when no mapping exists or hasn't been resolved yet.
   */
  static async getRealIdFor(aggregateId: string, candidateId: string): Promise<string> {
    const entry = await db.contractionIdMap.get(candidateId);
    if (entry && entry.aggregateId === aggregateId && entry.realId) {
      return entry.realId;
    }
    return candidateId;
  }

  /**
   * Cleanup mappings for an aggregate if needed.
   */
  static async clearForAggregate(aggregateId: string): Promise<void> {
    const toDelete = await db.contractionIdMap
      .where('aggregateId')
      .equals(aggregateId)
      .primaryKeys();
    if (toDelete.length) {
      await db.contractionIdMap.bulkDelete(toDelete as string[]);
    }
  }
}
