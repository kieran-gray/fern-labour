// Main exports for offline-first functionality
export { useOfflineMutation, useOnlineMutation } from './useOfflineMutation';
export { useSyncEngine, useSyncTrigger, useSyncIndicator } from './useSyncEngine';

// Re-export utilities and types
export { OutboxManager } from '../storage/outbox';
export { networkDetector, useNetworkState } from '../sync/networkDetector';
export { syncEngine } from '../sync/syncEngine';
export { initializeDatabase, clearAllData, getDatabaseStats } from '../storage/database';
export { clearQueryPersistence, getQueryCacheStats } from '../persistence/queryPersistence';

// Export types for TypeScript support
export type { OutboxEvent, SequenceCounter } from '../storage/database';
export type { NetworkState } from '../sync/networkDetector';
export type { EventType } from '../storage/outbox';
