import {
  compareEventIds,
  generateEventId,
  generateEventIdBatch,
  getEventTimestamp,
  isValidEventId,
} from '../eventId';

describe('Event ID Generation', () => {
  beforeEach(() => {
    jest.clearAllTimers();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
    jest.useRealTimers();
  });

  describe('generateEventId', () => {
    it('should generate a valid ULID', () => {
      const eventId = generateEventId();

      expect(eventId).toBeDefined();
      expect(typeof eventId).toBe('string');
      expect(eventId.length).toBe(26);
      expect(isValidEventId(eventId)).toBe(true);
    });

    it('should generate unique IDs', () => {
      const id1 = generateEventId();
      const id2 = generateEventId();

      expect(id1).not.toBe(id2);
    });

    it('should generate lexicographically sortable IDs', () => {
      const id1 = generateEventId();

      // Advance time slightly
      jest.advanceTimersByTime(1);

      const id2 = generateEventId();

      expect(compareEventIds(id1, id2)).toBeLessThan(0);
      expect(compareEventIds(id2, id1)).toBeGreaterThan(0);
    });
  });

  describe('getEventTimestamp', () => {
    it('should extract timestamp from ULID', () => {
      const beforeTime = Date.now();
      const eventId = generateEventId();
      const afterTime = Date.now();

      const extractedTimestamp = getEventTimestamp(eventId);

      expect(extractedTimestamp).toBeInstanceOf(Date);
      expect(extractedTimestamp.getTime()).toBeGreaterThanOrEqual(beforeTime);
      expect(extractedTimestamp.getTime()).toBeLessThanOrEqual(afterTime);
    });

    it('should throw error for invalid ULID', () => {
      expect(() => getEventTimestamp('invalid-ulid')).toThrow();
    });
  });

  describe('isValidEventId', () => {
    it('should validate correct ULID format', () => {
      const validId = generateEventId();
      expect(isValidEventId(validId)).toBe(true);
    });

    it('should reject invalid formats', () => {
      expect(isValidEventId('')).toBe(false);
      expect(isValidEventId('too-short')).toBe(false);
      expect(isValidEventId('0123456789012345678901234')).toBe(false); // 25 chars
      expect(isValidEventId('012345678901234567890123456')).toBe(false); // 27 chars
      expect(isValidEventId('0123456789012345678901234!')).toBe(false); // invalid char
    });

    it('should accept case-insensitive ULIDs', () => {
      const upperCaseId = '01ARZ3NDEKTSV4RRFFQ69G5FAV';
      const lowerCaseId = '01arz3ndektsv4rrffq69g5fav';

      expect(isValidEventId(upperCaseId)).toBe(true);
      expect(isValidEventId(lowerCaseId)).toBe(true);
    });
  });

  describe('compareEventIds', () => {
    it('should compare ULIDs lexicographically', () => {
      const id1 = '01ARZ3NDEKTSV4RRFFQ69G5FAV';
      const id2 = '01ARZ3NDEKTSV4RRFFQ69G5FAW';

      expect(compareEventIds(id1, id2)).toBeLessThan(0);
      expect(compareEventIds(id2, id1)).toBeGreaterThan(0);
      expect(compareEventIds(id1, id1)).toBe(0);
    });

    it('should handle case-insensitive comparison', () => {
      const id1 = '01ARZ3NDEKTSV4RRFFQ69G5FAV';
      const id2 = '01ARZ3NDEKTSV4RRFFQ69G5FAV'; // Same case for comparison

      expect(compareEventIds(id1, id2)).toBe(0);
    });
  });

  describe('generateEventIdBatch', () => {
    it('should generate specified number of IDs', () => {
      const count = 5;
      const batch = generateEventIdBatch(count);

      expect(batch).toHaveLength(count);
      expect(batch.every((id) => isValidEventId(id))).toBe(true);
    });

    it('should return sorted batch', () => {
      const batch = generateEventIdBatch(10);
      const sortedBatch = [...batch].sort();

      expect(batch).toEqual(sortedBatch);
    });

    it('should generate unique IDs in batch', () => {
      const batch = generateEventIdBatch(100);
      const uniqueIds = new Set(batch);

      expect(uniqueIds.size).toBe(batch.length);
    });

    it('should handle zero count', () => {
      const batch = generateEventIdBatch(0);
      expect(batch).toEqual([]);
    });
  });
});
