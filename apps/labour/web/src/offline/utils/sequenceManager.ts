import { db, SequenceCounter } from '../storage/database';

/**
 * Manages per-aggregate sequence numbers for event ordering
 * Ensures strict ordering within each labour aggregate
 */
export class SequenceManager {
  /**
   * Get the next sequence number for an aggregate
   * Creates the counter if it doesn't exist
   */
  static async getNextSequence(aggregateId: string): Promise<number> {
    return await db.transaction('rw', db.sequences, async () => {
      const counter = await db.sequences.get(aggregateId);

      if (counter) {
        const nextSequence = counter.sequence + 1;
        await db.sequences.update(aggregateId, { sequence: nextSequence });
        return nextSequence;
      }
      const newCounter: SequenceCounter = {
        aggregateId,
        sequence: 1,
      };
      await db.sequences.add(newCounter);
      return 1;
    });
  }

  /**
   * Get current sequence number without incrementing
   */
  static async getCurrentSequence(aggregateId: string): Promise<number> {
    const counter = await db.sequences.get(aggregateId);
    return counter?.sequence || 0;
  }

  /**
   * Reset sequence counter for an aggregate
   * Useful during testing or aggregate recreation
   */
  static async resetSequence(aggregateId: string): Promise<void> {
    await db.sequences.delete(aggregateId);
  }

  /**
   * Set specific sequence number for an aggregate
   * Useful when syncing with server state or recovering from conflicts
   */
  static async setSequence(aggregateId: string, sequence: number): Promise<void> {
    await db.sequences.put({
      aggregateId,
      sequence,
    });
  }

  /**
   * Get all sequence counters (for debugging/monitoring)
   */
  static async getAllSequences(): Promise<SequenceCounter[]> {
    return await db.sequences.toArray();
  }

  /**
   * Clean up sequence counters for aggregates that no longer exist
   * This can be called periodically to maintain database hygiene
   */
  static async cleanupOrphanedSequences(existingAggregateIds: string[]): Promise<void> {
    const allSequences = await db.sequences.toArray();
    const orphanedIds = allSequences
      .map((seq) => seq.aggregateId)
      .filter((id) => !existingAggregateIds.includes(id));

    if (orphanedIds.length > 0) {
      await db.sequences.bulkDelete(orphanedIds);
    }
  }
}
