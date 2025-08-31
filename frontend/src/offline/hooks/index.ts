// Main exports for offline-first functionality
export { useOfflineMutation, useOnlineMutation } from './useOfflineMutation';
export { useGuestMode, useIsGuestMode, GuestModeProvider } from './useGuestMode';
export { useSyncEngine, useSyncTrigger, useSyncIndicator } from './useSyncEngine';

// Re-export utilities and types
export { OutboxManager } from '../storage/outbox';
export { GuestProfileManager } from '../storage/guestProfile';
export { networkDetector, useNetworkState } from '../sync/networkDetector';
export { syncEngine } from '../sync/syncEngine';
export { initializeDatabase, clearAllData, getDatabaseStats } from '../storage/database';
export { clearQueryPersistence, getQueryCacheStats } from '../persistence/queryPersistence';

// Export types for TypeScript support
export type { OutboxEvent, GuestProfile, SequenceCounter } from '../storage/database';
export type { NetworkState } from '../sync/networkDetector';
export type { EventType } from '../storage/outbox';
