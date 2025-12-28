/**
 * Sync Manager
 * Replays queued commands when back online
 */

import { useEffect, useState } from 'react';
import type { LabourServiceV2Client } from '@base/clients/labour_service';
import { getPendingCommands, getPendingCount, removeCommand } from './commandQueue';
import { networkDetector } from './sync/networkDetector';

type SyncStatus = 'idle' | 'syncing' | 'error';

interface SyncState {
  status: SyncStatus;
  pendingCount: number;
  lastError?: string;
}

type SyncListener = (state: SyncState) => void;

class SyncManager {
  private client: LabourServiceV2Client | null = null;
  private isSyncing = false;
  private listeners = new Set<SyncListener>();
  private state: SyncState = { status: 'idle', pendingCount: 0 };

  /**
   * Initialize the sync manager with a client
   * Must be called before sync can happen
   */
  initialize(client: LabourServiceV2Client) {
    this.client = client;

    // Listen for network changes
    networkDetector.subscribe((networkState) => {
      if (networkState.isOnline && !this.isSyncing) {
        // Small delay to let connection stabilize
        setTimeout(() => this.sync(), 1000);
      }
    });

    // Initial sync if online
    if (navigator.onLine) {
      this.sync();
    }

    // Update pending count
    this.updatePendingCount();
  }

  /**
   * Subscribe to sync state changes
   */
  subscribe(listener: SyncListener): () => void {
    this.listeners.add(listener);
    listener(this.state);
    return () => this.listeners.delete(listener);
  }

  /**
   * Trigger a sync attempt
   */
  async sync(): Promise<void> {
    if (!this.client || this.isSyncing || !navigator.onLine) {
      return;
    }

    this.isSyncing = true;
    this.updateState({ status: 'syncing' });

    try {
      const commands = await getPendingCommands();

      for (const queuedCommand of commands) {
        if (!navigator.onLine) {
          break; // Stop if we go offline during sync
        }

        try {
          // Send the command directly to the API
          const response = await this.executeCommand(queuedCommand.command);

          if (response.success) {
            await removeCommand(queuedCommand.id);
          } else {
            // Command failed - could be a conflict or validation error
            // For now, remove it anyway to prevent stuck queue
            // In production, you might want to handle conflicts differently
            console.warn('[SyncManager] Command failed:', response.error);
            await removeCommand(queuedCommand.id);
          }
        } catch (error) {
          // Network error - stop syncing
          console.error('[SyncManager] Sync error:', error);
          this.updateState({
            status: 'error',
            lastError: error instanceof Error ? error.message : 'Sync failed',
          });
          break;
        }
      }

      await this.updatePendingCount();
      if (this.state.pendingCount === 0) {
        this.updateState({ status: 'idle', lastError: undefined });
      }
    } finally {
      this.isSyncing = false;
    }
  }

  /**
   * Execute a command against the API
   */
  private async executeCommand(command: unknown): Promise<{ success: boolean; error?: string }> {
    if (!this.client) {
      return { success: false, error: 'Client not initialized' };
    }

    try {
      // Use fetch directly since we need to bypass websocket for queued commands
      // Access private config via bracket notation
      const clientConfig = (
        this.client as unknown as {
          config: { getAccessToken?: () => Promise<string | null>; baseUrl?: string };
        }
      ).config;
      const token = clientConfig?.getAccessToken ? await clientConfig.getAccessToken() : null;

      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      if (token) {
        headers.Authorization = `Bearer ${token}`;
      }

      const baseUrl = clientConfig?.baseUrl || '';
      const response = await fetch(`${baseUrl}/api/v1/command`, {
        method: 'POST',
        headers,
        body: JSON.stringify(command),
      });

      if (!response.ok) {
        const errorText = await response.text();
        return { success: false, error: errorText };
      }

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  private async updatePendingCount(): Promise<void> {
    try {
      const count = await getPendingCount();
      this.updateState({ pendingCount: count });
    } catch {
      // Ignore errors
    }
  }

  private updateState(partial: Partial<SyncState>): void {
    this.state = { ...this.state, ...partial };
    this.listeners.forEach((listener) => {
      try {
        listener(this.state);
      } catch {
        // Ignore listener errors
      }
    });
  }

  /**
   * Get current sync state
   */
  getState(): SyncState {
    return this.state;
  }

  /**
   * Force refresh pending count
   */
  async refreshPendingCount(): Promise<number> {
    await this.updatePendingCount();
    return this.state.pendingCount;
  }
}

// Singleton instance
export const syncManager = new SyncManager();

/**
 * React hook for sync state
 */
export function useSyncState(): SyncState {
  const [state, setState] = useState<SyncState>(syncManager.getState());

  useEffect(() => {
    return syncManager.subscribe(setState);
  }, []);

  return state;
}
