import {
  CompleteLabourRequest,
  ContractionsService,
  DeleteContractionRequest,
  EndContractionRequest,
  LabourService,
  LabourUpdateRequest,
  LabourUpdatesService,
  PlanLabourRequest,
  StartContractionRequest,
  UpdateContractionRequest,
} from '@clients/labour_service';
import { OutboxEvent } from '../hooks';
import { OutboxManager } from '../storage/outbox';
import { offlineLogger } from '../utils/logger';
import { networkDetector, NetworkState } from './networkDetector';

/**
 * Sync engine for replaying events to server in order
 * Handles per-aggregate concurrency and retry logic
 */
export class SyncEngine {
  private activeSyncs = new Set<string>();
  private retryTimers = new Map<string, NodeJS.Timeout>();
  private isRunning = false;
  private eventDelayMs: number;

  constructor() {
    this.eventDelayMs = this.resolveEventDelay();
    this.setupNetworkListener();
  }

  /**
   * Start the sync engine
   */
  start(): void {
    if (this.isRunning) {
      return;
    }

    this.isRunning = true;

    if (networkDetector.getState().isOnline) {
      this.triggerSync();
    }
    offlineLogger.info('sync:start');
  }

  /**
   * Stop the sync engine and clear timers
   */
  stop(): void {
    this.isRunning = false;
    this.activeSyncs.clear();

    this.retryTimers.forEach((timer) => clearTimeout(timer));
    this.retryTimers.clear();
    offlineLogger.info('sync:stop');
  }

  /**
   * Trigger sync for all pending events
   */
  async triggerSync(): Promise<void> {
    if (!this.isRunning || !networkDetector.isSyncable()) {
      return;
    }

    try {
      // Get all aggregates with pending events
      const pendingEvents = await OutboxManager.getAllPendingEvents();
      const aggregateIds = [...new Set(pendingEvents.map((e) => e.aggregateId))];

      // Sync each aggregate independently
      const syncPromises = aggregateIds.map((aggregateId) => this.syncAggregate(aggregateId));

      await Promise.allSettled(syncPromises);
      offlineLogger.debug('sync:trigger', {
        aggregates: aggregateIds.length,
        pending: pendingEvents.length,
      });
    } catch (error) {
      // Do nothing
    }
  }

  /**
   * Sync specific aggregate in sequence order
   */
  async syncAggregate(aggregateId: string): Promise<void> {
    if (this.activeSyncs.has(aggregateId) || !networkDetector.isSyncable()) {
      return;
    }

    this.activeSyncs.add(aggregateId);
    offlineLogger.debug('sync:aggregate:start', { aggregateId });

    try {
      const pendingEvents = await OutboxManager.getPendingEvents(aggregateId);

      if (pendingEvents.length === 0) {
        return;
      }

      for (const event of pendingEvents) {
        if (!networkDetector.isSyncable()) {
          break;
        }
        const ok = await this.syncEvent(event);
        if (!ok) {
          break;
        }
        await this.delayBetweenEvents(event);
      }
    } finally {
      this.activeSyncs.delete(aggregateId);
      offlineLogger.debug('sync:aggregate:end', { aggregateId });
    }
  }

  /**
   * Sync individual event to server
   */
  private async syncEvent(event: OutboxEvent): Promise<boolean> {
    try {
      await OutboxManager.markEventSyncing(event.id);
      await this.executeEvent(event);
      await OutboxManager.markEventSynced(event.id);
      offlineLogger.info('sync:event:success', {
        id: event.id,
        type: event.eventType,
        seq: event.sequence,
        aggregateId: event.aggregateId,
      });
      return true;
    } catch (error) {
      await OutboxManager.markEventFailed(event.id, String(error));
      this.scheduleRetry(event);
      offlineLogger.warn('sync:event:failed', {
        id: event.id,
        type: event.eventType,
        seq: event.sequence,
        aggregateId: event.aggregateId,
        error: String(error),
      });
      return false;
    }
  }

  /**
   * Execute event against appropriate service
   */
  private async executeEvent(event: OutboxEvent): Promise<any> {
    const payload = event.payload as any;

    switch (event.eventType) {
      case 'plan_labour':
        return await LabourService.planLabour({
          requestBody: payload as PlanLabourRequest,
        });

      case 'complete_labour':
        return await LabourService.completeLabour({
          requestBody: payload as CompleteLabourRequest,
        });

      case 'start_contraction':
        return await ContractionsService.startContraction({
          requestBody: payload as StartContractionRequest,
        });

      case 'end_contraction':
        return await ContractionsService.endContraction({
          requestBody: payload as EndContractionRequest,
        });

      case 'update_contraction':
        return await ContractionsService.updateContraction({
          requestBody: payload as UpdateContractionRequest,
        });

      case 'delete_contraction':
        return await ContractionsService.deleteContraction({
          requestBody: payload as DeleteContractionRequest,
        });

      case 'labour_update':
        return await LabourUpdatesService.postLabourUpdate({
          requestBody: payload as LabourUpdateRequest,
        });

      default:
        throw new Error(`Unknown event type: ${event.eventType}`);
    }
  }

  /**
   * Schedule retry with exponential backoff
   */
  private scheduleRetry(event: OutboxEvent): void {
    const retryDelay = Math.min(1000 * 2 ** (event.retryCount + 1), 30000); // Max 30s
    const eventKey = `${event.aggregateId}-${event.sequence}`;

    // Clear existing timer
    if (this.retryTimers.has(eventKey)) {
      clearTimeout(this.retryTimers.get(eventKey)!);
    }

    // Schedule retry
    const timer = setTimeout(async () => {
      this.retryTimers.delete(eventKey);

      if (networkDetector.isSyncable()) {
        await OutboxManager.retryEvent(event.id);
        await this.syncAggregate(event.aggregateId);
      }
    }, retryDelay);

    this.retryTimers.set(eventKey, timer);
    offlineLogger.info('sync:retry:scheduled', { id: event.id, inMs: retryDelay });
  }

  private async delayBetweenEvents(event: OutboxEvent): Promise<void> {
    const ms = this.eventDelayMs;
    if (!ms || ms <= 0) {
      return;
    }
    offlineLogger.debug('sync:aggregate:delay', {
      aggregateId: event.aggregateId,
      seq: event.sequence,
      ms,
    });
    await new Promise((resolve) => setTimeout(resolve, ms));
  }

  private resolveEventDelay(): number {
    try {
      if (typeof window !== 'undefined') {
        const win = window as any;
        if (typeof win.__OFFLINE_SYNC_DELAY_MS === 'number') {
          return win.__OFFLINE_SYNC_DELAY_MS;
        }
        const fromLs = window.localStorage?.getItem('OFFLINE_SYNC_DELAY_MS');
        if (fromLs) {
          return parseInt(fromLs, 10) || 0;
        }
      }
    } catch {
      // Do nothing
    }
    if (typeof process !== 'undefined' && (process as any).env) {
      const env: any = (process as any).env;
      if (env.NODE_ENV === 'test') {
        return 0;
      }
      const v = env.VITE_OFFLINE_SYNC_DELAY_MS || env.OFFLINE_SYNC_DELAY_MS;
      if (v) {
        return parseInt(v as string, 10) || 0;
      }
    }
    return 150;
  }

  /**
   * Setup network state listener
   */
  private setupNetworkListener(): void {
    networkDetector.subscribe((state: NetworkState) => {
      if (state.isOnline && this.isRunning) {
        offlineLogger.info('sync:network:online');
        setTimeout(() => this.triggerSync(), 1000);
      }
    });
  }

  /**
   * Get sync status for monitoring
   */
  async getSyncStatus() {
    const stats = await OutboxManager.getStats();

    return {
      ...stats,
      activeSyncs: this.activeSyncs.size,
      scheduledRetries: this.retryTimers.size,
      isRunning: this.isRunning,
      isOnline: networkDetector.getState().isOnline,
    };
  }

  /**
   * Force retry all failed events
   */
  async retryFailedEvents(): Promise<void> {
    const failedEvents = await OutboxManager.getRetriableEvents();

    for (const event of failedEvents) {
      await OutboxManager.retryEvent(event.id);
    }

    if (failedEvents.length > 0) {
      offlineLogger.info('sync:retry:resetFailed', { count: failedEvents.length });
      await this.triggerSync();
    }
  }
}

/**
 * Singleton sync engine instance
 */
const g = globalThis as any;
if (!g.__FERN_SYNC_ENGINE__) {
  g.__FERN_SYNC_ENGINE__ = new SyncEngine();
}
export const syncEngine: SyncEngine = g.__FERN_SYNC_ENGINE__;
