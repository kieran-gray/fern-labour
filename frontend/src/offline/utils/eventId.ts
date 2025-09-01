import { ulid } from 'ulid';

/**
 * Generate a unique, sortable event ID using ULID (Universally Unique Lexicographically Sortable Identifier)
 *
 * ULIDs provide:
 * - 128-bit compatibility with UUID
 * - Lexicographically sortable by timestamp
 * - Case insensitive encoding
 * - Crockford's base32 for better human readability
 * - Monotonic sort order within the same millisecond
 */
export function generateEventId(): string {
  return ulid();
}

/**
 * Extract timestamp from a ULID event ID
 * Useful for debugging and ordering verification
 */
export function getEventTimestamp(eventId: string): Date {
  const timestampPart = eventId.substring(0, 10);
  const timestamp = decodeBase32(timestampPart);
  return new Date(timestamp);
}

/**
 * Validate if a string is a valid ULID
 */
export function isValidEventId(eventId: string): boolean {
  const ulidRegex = /^[0-9A-HJKMNP-TV-Z]{26}$/i;
  return ulidRegex.test(eventId);
}

/**
 * Compare two event IDs for ordering
 * Returns negative if a < b, positive if a > b, zero if equal
 */
export function compareEventIds(a: string, b: string): number {
  return a.localeCompare(b);
}

/**
 * Simple base32 decoder for ULID timestamp extraction
 * Based on Crockford's base32
 */
function decodeBase32(encoded: string): number {
  const alphabet = '0123456789ABCDEFGHJKMNPQRSTVWXYZ';
  let decoded = 0;

  for (let i = 0; i < encoded.length; i++) {
    const char = encoded.charAt(i).toUpperCase();
    const value = alphabet.indexOf(char);

    if (value === -1) {
      throw new Error(`Invalid character in ULID: ${char}`);
    }

    decoded = decoded * 32 + value;
  }

  return decoded;
}

/**
 * Generate a batch of sequential event IDs within the same millisecond
 * Useful for maintaining order when multiple events are created simultaneously
 */
export function generateEventIdBatch(count: number): string[] {
  const ids: string[] = [];

  for (let i = 0; i < count; i++) {
    ids.push(ulid());
  }

  return ids.sort();
}
