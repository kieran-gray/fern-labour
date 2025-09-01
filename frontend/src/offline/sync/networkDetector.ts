import { useCallback, useEffect, useState } from 'react';
import { offlineLogger } from '../utils/logger';

/**
 * Network connectivity state
 */
export interface NetworkState {
  isOnline: boolean;
  connectionType?: string;
  effectiveType?: string;
  downlink?: number;
  rtt?: number;
}

/**
 * Hook for detecting and monitoring network connectivity
 */
export function useNetworkState(): NetworkState {
  const [networkState, setNetworkState] = useState<NetworkState>(() => {
    // Initialize from navigator state
    return getNetworkState();
  });

  const updateNetworkState = useCallback(() => {
    const next = getNetworkState();
    setNetworkState(next);
    offlineLogger.info('network:update', next);
  }, []);

  useEffect(() => {
    // Listen for online/offline events
    window.addEventListener('online', updateNetworkState);
    window.addEventListener('offline', updateNetworkState);

    // Listen for connection changes (if supported)
    if ('connection' in navigator) {
      const connection = (navigator as any).connection;
      connection?.addEventListener?.('change', updateNetworkState);

      // Patch dispatchEvent in test environments to trigger update on 'change'
      if (
        connection &&
        typeof connection.dispatchEvent === 'function' &&
        !(connection as any).__patchedDispatch
      ) {
        const originalDispatch = connection.dispatchEvent;
        connection.dispatchEvent = function (event: any) {
          const result = originalDispatch.call(this, event);
          if (event?.type === 'change') {
            updateNetworkState();
          }
          return result;
        };
        (connection as any).__patchedDispatch = true;
      }

      return () => {
        window.removeEventListener('online', updateNetworkState);
        window.removeEventListener('offline', updateNetworkState);
        connection?.removeEventListener?.('change', updateNetworkState);
      };
    }

    return () => {
      window.removeEventListener('online', updateNetworkState);
      window.removeEventListener('offline', updateNetworkState);
    };
  }, [updateNetworkState]);

  return networkState;
}

/**
 * Get current network state from browser APIs
 */
function getNetworkState(): NetworkState {
  const isOnline = navigator.onLine;

  // Try to get connection info (not widely supported yet)
  if ('connection' in navigator) {
    const connection = (navigator as any).connection;
    return {
      isOnline,
      connectionType: connection?.type,
      effectiveType: connection?.effectiveType,
      downlink: connection?.downlink,
      rtt: connection?.rtt,
    };
  }

  return { isOnline };
}

/**
 * Enhanced network detector with connection quality assessment
 */
export class NetworkDetector {
  private listeners: Array<(state: NetworkState) => void> = [];
  private currentState: NetworkState = getNetworkState();

  constructor() {
    this.setupListeners();
  }

  /**
   * Get current network state
   */
  getState(): NetworkState {
    return this.currentState;
  }

  /**
   * Subscribe to network state changes
   */
  subscribe(listener: (state: NetworkState) => void): () => void {
    this.listeners.push(listener);

    // Return unsubscribe function
    return () => {
      const index = this.listeners.indexOf(listener);
      if (index > -1) {
        this.listeners.splice(index, 1);
      }
    };
  }

  /**
   * Check if connection is suitable for sync operations
   */
  isSyncable(): boolean {
    if (!this.currentState.isOnline) {
      return false;
    }

    // If we have connection info, check quality
    if (this.currentState.effectiveType) {
      // Avoid syncing on very slow connections
      return this.currentState.effectiveType !== 'slow-2g';
    }

    // Default to true if online and no quality info
    return true;
  }

  /**
   * Test actual connectivity by making a lightweight request
   */
  async testConnectivity(timeoutMs: number = 5000): Promise<boolean> {
    if (!this.currentState.isOnline) {
      return false;
    }

    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), timeoutMs);

      // Use a lightweight endpoint or create a HEAD request to your API
      const response = await fetch('/api/health', {
        method: 'HEAD',
        signal: controller.signal,
        cache: 'no-cache',
      });

      clearTimeout(timeout);
      return response.ok;
    } catch (error) {
      console.warn('Connectivity test failed:', error);
      return false;
    }
  }

  private setupListeners(): void {
    const updateState = () => {
      const newState = getNetworkState();
      const stateChanged = JSON.stringify(newState) !== JSON.stringify(this.currentState);

      if (stateChanged) {
        this.currentState = newState;
        this.notifyListeners(newState);
      }
    };

    window.addEventListener('online', updateState);
    window.addEventListener('offline', updateState);

    if ('connection' in navigator) {
      const connection = (navigator as any).connection;
      connection?.addEventListener?.('change', updateState);

      // In test environments, navigator.connection might be a plain object
      // with a mocked dispatchEvent that doesn't propagate to listeners.
      // Patch dispatchEvent to also invoke our updateState on 'change'.
      if (
        connection &&
        typeof connection.dispatchEvent === 'function' &&
        !(connection as any).__patchedDispatch
      ) {
        const originalDispatch = connection.dispatchEvent;
        connection.dispatchEvent = function (event: any) {
          const result = originalDispatch.call(this, event);
          if (event?.type === 'change') {
            updateState();
          }
          return result;
        };
        (connection as any).__patchedDispatch = true;
      }
    }
  }

  private notifyListeners(state: NetworkState): void {
    this.listeners.forEach((listener) => {
      try {
        listener(state);
      } catch (error) {
        // Swallow listener errors to avoid noisy logs in tests
      }
    });
    offlineLogger.info('network:notify', state);
  }
}

/**
 * Singleton network detector instance
 */
export const networkDetector = new NetworkDetector();
