import { useSyncEngineContext } from './SyncEngineProvider';

/**
 * Hook for managing and monitoring the sync engine
 */
export function useSyncEngine() {
  return useSyncEngineContext();
}

/**
 * Simplified hook just for triggering sync
 */
export function useSyncTrigger() {
  const { triggerSync } = useSyncEngineContext();
  return { triggerSync };
}

/**
 * Hook for sync status indicators in UI
 */
export function useSyncIndicator() {
  const { syncStatus, hasUnsynced, isActivelySyncing, needsAttention } = useSyncEngineContext();

  let indicatorState: 'synced' | 'syncing' | 'offline' | 'failed' = 'synced';
  let message = 'All changes synced';

  if (!syncStatus.isOnline) {
    indicatorState = 'offline';
    message = hasUnsynced
      ? `${syncStatus.pendingEvents} changes will sync when online`
      : 'Offline - ready to track';
  } else if (needsAttention) {
    indicatorState = 'failed';
    message = `${syncStatus.failedEvents} changes failed to sync`;
  } else if (isActivelySyncing) {
    indicatorState = 'syncing';
    message = 'Syncing changes...';
  } else if (hasUnsynced) {
    indicatorState = 'syncing';
    message = `Syncing ${syncStatus.pendingEvents} changes...`;
  }

  return {
    state: indicatorState,
    message,
    pendingCount: syncStatus.pendingEvents,
    failedCount: syncStatus.failedEvents,
  };
}
