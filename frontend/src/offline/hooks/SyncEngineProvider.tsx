import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { OutboxManager } from '../storage/outbox';
import { useNetworkState } from '../sync/networkDetector';
import { syncEngine } from '../sync/syncEngine';
import { offlineLogger } from '../utils/logger';

interface SyncStatus {
  isRunning: boolean;
  isOnline: boolean;
  pendingEvents: number;
  syncingEvents: number;
  failedEvents: number;
  activeSyncs: number;
  scheduledRetries: number;
}

interface SyncEngineContextValue {
  syncStatus: SyncStatus;
  triggerSync: () => Promise<void>;
  retryFailedEvents: () => Promise<void>;
  pruneSyncedEvents: () => Promise<number>;
  hasUnsynced: boolean;
  isActivelySyncing: boolean;
  needsAttention: boolean;
  isHealthy: boolean;
}

const SyncEngineContext = createContext<SyncEngineContextValue | null>(null);

export function SyncEngineProvider({ children }: { children: React.ReactNode }) {
  const [syncStatus, setSyncStatus] = useState<SyncStatus>({
    isRunning: false,
    isOnline: false,
    pendingEvents: 0,
    syncingEvents: 0,
    failedEvents: 0,
    activeSyncs: 0,
    scheduledRetries: 0,
  });

  const networkState = useNetworkState();

  const updateSyncStatus = useCallback(async () => {
    const status = await syncEngine.getSyncStatus();
    setSyncStatus({
      isRunning: status.isRunning,
      isOnline: status.isOnline,
      pendingEvents: status.pending,
      syncingEvents: status.syncing,
      failedEvents: status.failed,
      activeSyncs: status.activeSyncs,
      scheduledRetries: status.scheduledRetries,
    });
  }, []);

  useEffect(() => {
    offlineLogger.info('sync:provider:mount');
    syncEngine.start();
    updateSyncStatus();
    // Expose a lightweight global refresher to allow push-updates from mutations
    (globalThis as any).__SYNC_REFRESH__ = updateSyncStatus;
    const interval = setInterval(updateSyncStatus, 5000);
    return () => {
      clearInterval(interval);
      try {
        delete (globalThis as any).__SYNC_REFRESH__;
      } catch {
        // Do nothing
      }
      offlineLogger.info('sync:provider:unmount');
    };
  }, [updateSyncStatus]);

  useEffect(() => {
    updateSyncStatus();
  }, [networkState.isOnline, updateSyncStatus]);

  const triggerSync = useCallback(async () => {
    await syncEngine.triggerSync();
    setTimeout(updateSyncStatus, 1000);
  }, [updateSyncStatus]);

  const retryFailedEvents = useCallback(async () => {
    await syncEngine.retryFailedEvents();
    setTimeout(updateSyncStatus, 1000);
  }, [updateSyncStatus]);

  const pruneSyncedEvents = useCallback(async () => {
    const prunedCount = await OutboxManager.pruneSyncedEvents();
    setTimeout(updateSyncStatus, 1000);
    return prunedCount;
  }, [updateSyncStatus]);

  const value = useMemo<SyncEngineContextValue>(() => {
    const hasUnsynced = syncStatus.pendingEvents + syncStatus.failedEvents > 0;
    const isActivelySyncing = syncStatus.syncingEvents > 0 || syncStatus.activeSyncs > 0;
    const needsAttention = syncStatus.failedEvents > 0;
    const isHealthy = syncStatus.isOnline && syncStatus.failedEvents === 0;
    return {
      syncStatus,
      triggerSync,
      retryFailedEvents,
      pruneSyncedEvents,
      hasUnsynced,
      isActivelySyncing,
      needsAttention,
      isHealthy,
    };
  }, [syncStatus, triggerSync, retryFailedEvents, pruneSyncedEvents]);

  return <SyncEngineContext.Provider value={value}>{children}</SyncEngineContext.Provider>;
}

export function useSyncEngineContext(): SyncEngineContextValue {
  const ctx = useContext(SyncEngineContext);
  if (!ctx) {
    throw new Error('useSyncEngineContext must be used within SyncEngineProvider');
  }
  return ctx;
}
