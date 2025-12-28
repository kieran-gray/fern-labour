/**
 * UUID v7 Generator
 *
 * UUID v7 is time-ordered and contains:
 * - 48 bits: Unix timestamp in milliseconds
 * - 4 bits: version (7)
 * - 12 bits: random
 * - 2 bits: variant
 * - 62 bits: random
 */

export function uuidv7(): string {
  const timestamp = Date.now();

  // Get random bytes
  const randomBytes = new Uint8Array(10);
  crypto.getRandomValues(randomBytes);

  // Build the UUID
  // Bytes 0-5: timestamp (48 bits)
  const timestampHex = timestamp.toString(16).padStart(12, '0');

  // Bytes 6-7: version (4 bits) + random (12 bits)
  // Version 7 = 0111
  const byte6 = 0x70 | (randomBytes[0] & 0x0f);
  const byte7 = randomBytes[1];

  // Bytes 8-9: variant (2 bits = 10) + random (14 bits)
  const byte8 = 0x80 | (randomBytes[2] & 0x3f);
  const byte9 = randomBytes[3];

  // Bytes 10-15: random (48 bits)
  const randomHex = Array.from(randomBytes.slice(4))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');

  // Format: xxxxxxxx-xxxx-7xxx-yxxx-xxxxxxxxxxxx
  return [
    timestampHex.slice(0, 8),
    timestampHex.slice(8, 12),
    byte6.toString(16).padStart(2, '0') + byte7.toString(16).padStart(2, '0'),
    byte8.toString(16).padStart(2, '0') + byte9.toString(16).padStart(2, '0'),
    randomHex,
  ].join('-');
}
