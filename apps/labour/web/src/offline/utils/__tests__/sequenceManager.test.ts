import { db } from '../../storage/database';
import { SequenceManager } from '../sequenceManager';

describe('SequenceManager', () => {
  beforeEach(async () => {
    // Clear database before each test
    await db.sequences.clear();
  });

  afterEach(async () => {
    // Clean up after tests
    await db.sequences.clear();
  });

  describe('getNextSequence', () => {
    it('should start sequence at 1 for new aggregate', async () => {
      const aggregateId = 'test-aggregate-1';

      const sequence = await SequenceManager.getNextSequence(aggregateId);

      expect(sequence).toBe(1);
    });

    it('should increment sequence for existing aggregate', async () => {
      const aggregateId = 'test-aggregate-1';

      const seq1 = await SequenceManager.getNextSequence(aggregateId);
      const seq2 = await SequenceManager.getNextSequence(aggregateId);
      const seq3 = await SequenceManager.getNextSequence(aggregateId);

      expect(seq1).toBe(1);
      expect(seq2).toBe(2);
      expect(seq3).toBe(3);
    });

    it('should handle multiple aggregates independently', async () => {
      const aggregate1 = 'test-aggregate-1';
      const aggregate2 = 'test-aggregate-2';

      const seq1_1 = await SequenceManager.getNextSequence(aggregate1);
      const seq2_1 = await SequenceManager.getNextSequence(aggregate2);
      const seq1_2 = await SequenceManager.getNextSequence(aggregate1);
      const seq2_2 = await SequenceManager.getNextSequence(aggregate2);

      expect(seq1_1).toBe(1);
      expect(seq2_1).toBe(1);
      expect(seq1_2).toBe(2);
      expect(seq2_2).toBe(2);
    });

    it('should handle concurrent access to same aggregate', async () => {
      const aggregateId = 'test-aggregate-1';

      // Simulate concurrent access
      const promises = Array.from({ length: 10 }, () =>
        SequenceManager.getNextSequence(aggregateId)
      );

      const sequences = await Promise.all(promises);

      // Should get unique sequential numbers
      const sortedSequences = sequences.sort((a, b) => a - b);
      expect(sortedSequences).toEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
    });
  });

  describe('getCurrentSequence', () => {
    it('should return 0 for non-existent aggregate', async () => {
      const aggregateId = 'non-existent';

      const currentSeq = await SequenceManager.getCurrentSequence(aggregateId);

      expect(currentSeq).toBe(0);
    });

    it('should return current sequence without incrementing', async () => {
      const aggregateId = 'test-aggregate-1';

      await SequenceManager.getNextSequence(aggregateId);
      await SequenceManager.getNextSequence(aggregateId);

      const currentSeq = await SequenceManager.getCurrentSequence(aggregateId);
      expect(currentSeq).toBe(2);

      // Should not increment
      const stillCurrentSeq = await SequenceManager.getCurrentSequence(aggregateId);
      expect(stillCurrentSeq).toBe(2);
    });
  });

  describe('resetSequence', () => {
    it('should reset sequence for aggregate', async () => {
      const aggregateId = 'test-aggregate-1';

      await SequenceManager.getNextSequence(aggregateId);
      await SequenceManager.getNextSequence(aggregateId);

      expect(await SequenceManager.getCurrentSequence(aggregateId)).toBe(2);

      await SequenceManager.resetSequence(aggregateId);

      expect(await SequenceManager.getCurrentSequence(aggregateId)).toBe(0);

      // Next sequence should start at 1 again
      const nextSeq = await SequenceManager.getNextSequence(aggregateId);
      expect(nextSeq).toBe(1);
    });

    it('should not affect other aggregates when resetting', async () => {
      const aggregate1 = 'test-aggregate-1';
      const aggregate2 = 'test-aggregate-2';

      await SequenceManager.getNextSequence(aggregate1);
      await SequenceManager.getNextSequence(aggregate2);
      await SequenceManager.getNextSequence(aggregate2);

      await SequenceManager.resetSequence(aggregate1);

      expect(await SequenceManager.getCurrentSequence(aggregate1)).toBe(0);
      expect(await SequenceManager.getCurrentSequence(aggregate2)).toBe(2);
    });
  });

  describe('setSequence', () => {
    it('should set specific sequence number', async () => {
      const aggregateId = 'test-aggregate-1';

      await SequenceManager.setSequence(aggregateId, 10);

      expect(await SequenceManager.getCurrentSequence(aggregateId)).toBe(10);

      const nextSeq = await SequenceManager.getNextSequence(aggregateId);
      expect(nextSeq).toBe(11);
    });

    it('should create counter if it does not exist', async () => {
      const aggregateId = 'new-aggregate';

      await SequenceManager.setSequence(aggregateId, 5);

      expect(await SequenceManager.getCurrentSequence(aggregateId)).toBe(5);
    });

    it('should update existing counter', async () => {
      const aggregateId = 'test-aggregate-1';

      await SequenceManager.getNextSequence(aggregateId);
      await SequenceManager.setSequence(aggregateId, 100);

      expect(await SequenceManager.getCurrentSequence(aggregateId)).toBe(100);
    });
  });

  describe('getAllSequences', () => {
    it('should return empty array when no sequences exist', async () => {
      const sequences = await SequenceManager.getAllSequences();
      expect(sequences).toEqual([]);
    });

    it('should return all sequence counters', async () => {
      const aggregate1 = 'test-aggregate-1';
      const aggregate2 = 'test-aggregate-2';

      await SequenceManager.getNextSequence(aggregate1);
      await SequenceManager.getNextSequence(aggregate1);
      await SequenceManager.getNextSequence(aggregate2);

      const sequences = await SequenceManager.getAllSequences();

      expect(sequences).toHaveLength(2);
      expect(sequences.find((s) => s.aggregateId === aggregate1)?.sequence).toBe(2);
      expect(sequences.find((s) => s.aggregateId === aggregate2)?.sequence).toBe(1);
    });
  });

  describe('cleanupOrphanedSequences', () => {
    it('should remove sequences not in the existing list', async () => {
      const aggregate1 = 'test-aggregate-1';
      const aggregate2 = 'test-aggregate-2';
      const aggregate3 = 'test-aggregate-3';

      await SequenceManager.getNextSequence(aggregate1);
      await SequenceManager.getNextSequence(aggregate2);
      await SequenceManager.getNextSequence(aggregate3);

      expect(await SequenceManager.getAllSequences()).toHaveLength(3);

      // Clean up, keeping only aggregate1 and aggregate3
      await SequenceManager.cleanupOrphanedSequences([aggregate1, aggregate3]);

      const remainingSequences = await SequenceManager.getAllSequences();
      expect(remainingSequences).toHaveLength(2);
      expect(remainingSequences.map((s) => s.aggregateId)).toEqual(
        expect.arrayContaining([aggregate1, aggregate3])
      );
      expect(remainingSequences.map((s) => s.aggregateId)).not.toContain(aggregate2);
    });

    it('should not remove any sequences if all exist', async () => {
      const aggregate1 = 'test-aggregate-1';
      const aggregate2 = 'test-aggregate-2';

      await SequenceManager.getNextSequence(aggregate1);
      await SequenceManager.getNextSequence(aggregate2);

      await SequenceManager.cleanupOrphanedSequences([aggregate1, aggregate2]);

      const sequences = await SequenceManager.getAllSequences();
      expect(sequences).toHaveLength(2);
    });

    it('should handle empty existing list', async () => {
      const aggregate1 = 'test-aggregate-1';

      await SequenceManager.getNextSequence(aggregate1);

      await SequenceManager.cleanupOrphanedSequences([]);

      const sequences = await SequenceManager.getAllSequences();
      expect(sequences).toHaveLength(0);
    });
  });
});
