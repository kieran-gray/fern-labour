import { act, renderHook } from '@testing-library/react';
import { NetworkDetector, useNetworkState } from '../networkDetector';

// Mock window events for deterministic testing
const simulateNetworkEvent = (type: 'online' | 'offline') => {
  const event = new Event(type);
  window.dispatchEvent(event);
};

const simulateConnectionChange = () => {
  if ('connection' in navigator && (navigator as any).connection) {
    const event = new Event('change');
    (navigator as any).connection.dispatchEvent(event);
  }
};

describe('NetworkDetector', () => {
  let originalConnection: any;

  beforeEach(() => {
    originalConnection = (navigator as any).connection;
    Object.defineProperty(navigator, 'onLine', { value: true, writable: true });
  });

  afterEach(() => {
    (navigator as any).connection = originalConnection;
  });

  describe('basic connectivity detection', () => {
    it('should detect online state', () => {
      const detector = new NetworkDetector();
      expect(detector.getState().isOnline).toBe(true);
    });

    it('should detect offline state', () => {
      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });

      const detector = new NetworkDetector();
      expect(detector.getState().isOnline).toBe(false);
    });

    it('should include connection details when available', () => {
      const mockConnection = {
        type: 'wifi',
        effectiveType: '4g',
        downlink: 10,
        rtt: 50,
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
      };
      (navigator as any).connection = mockConnection;

      const detector = new NetworkDetector();
      const state = detector.getState();

      expect(state).toEqual({
        isOnline: true,
        connectionType: 'wifi',
        effectiveType: '4g',
        downlink: 10,
        rtt: 50,
      });
    });

    it('should work gracefully without connection API', () => {
      delete (navigator as any).connection;

      const detector = new NetworkDetector();
      expect(detector.getState()).toEqual({ isOnline: true });
    });
  });

  describe('state change detection', () => {
    it('should detect transition to offline', () => {
      const detector = new NetworkDetector();
      const listener = jest.fn();

      detector.subscribe(listener);

      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });
      simulateNetworkEvent('offline');

      expect(listener).toHaveBeenCalledWith({ isOnline: false });
    });

    it('should detect transition to online', () => {
      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });
      const detector = new NetworkDetector();
      const listener = jest.fn();

      detector.subscribe(listener);

      Object.defineProperty(navigator, 'onLine', { value: true, writable: true });
      simulateNetworkEvent('online');

      expect(listener).toHaveBeenCalledWith({ isOnline: true });
    });

    it('should detect connection quality changes', () => {
      const mockConnection = {
        type: 'wifi',
        effectiveType: '4g',
        downlink: 10,
        rtt: 50,
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
      };
      (navigator as any).connection = mockConnection;

      const detector = new NetworkDetector();
      const listener = jest.fn();

      detector.subscribe(listener);

      // Change connection properties
      mockConnection.effectiveType = '3g';
      mockConnection.downlink = 2;

      simulateConnectionChange();

      expect(listener).toHaveBeenCalledWith({
        isOnline: true,
        connectionType: 'wifi',
        effectiveType: '3g',
        downlink: 2,
        rtt: 50,
      });
    });

    it('should not notify on identical state changes', () => {
      const detector = new NetworkDetector();
      const listener = jest.fn();

      detector.subscribe(listener);

      // Simulate same state change
      simulateNetworkEvent('online'); // Already online

      expect(listener).not.toHaveBeenCalled();
    });
  });

  describe('subscription management', () => {
    it('should support multiple subscribers', () => {
      const detector = new NetworkDetector();
      const listener1 = jest.fn();
      const listener2 = jest.fn();

      detector.subscribe(listener1);
      detector.subscribe(listener2);

      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });
      simulateNetworkEvent('offline');

      expect(listener1).toHaveBeenCalledWith({ isOnline: false });
      expect(listener2).toHaveBeenCalledWith({ isOnline: false });
    });

    it('should allow unsubscribing', () => {
      const detector = new NetworkDetector();
      const listener = jest.fn();

      const unsubscribe = detector.subscribe(listener);
      unsubscribe();

      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });
      simulateNetworkEvent('offline');

      expect(listener).not.toHaveBeenCalled();
    });

    it('should handle listener errors gracefully', () => {
      const detector = new NetworkDetector();
      const errorListener = jest.fn(() => {
        throw new Error('Listener error');
      });
      const workingListener = jest.fn();

      detector.subscribe(errorListener);
      detector.subscribe(workingListener);

      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });
      expect(() => simulateNetworkEvent('offline')).not.toThrow();
      expect(workingListener).toHaveBeenCalledWith({ isOnline: false });
    });
  });

  describe('sync suitability assessment', () => {
    it('should reject offline connections', () => {
      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });

      const detector = new NetworkDetector();
      expect(detector.isSyncable()).toBe(false);
    });

    it('should accept good online connections', () => {
      const mockConnection = {
        effectiveType: '4g',
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
      };
      (navigator as any).connection = mockConnection;

      const detector = new NetworkDetector();
      expect(detector.isSyncable()).toBe(true);
    });

    it('should reject very slow connections', () => {
      const mockConnection = {
        effectiveType: 'slow-2g',
        addEventListener: jest.fn(),
        removeEventListener: jest.fn(),
      };
      (navigator as any).connection = mockConnection;

      const detector = new NetworkDetector();
      expect(detector.isSyncable()).toBe(false);
    });

    it('should default to syncable when connection info unavailable', () => {
      delete (navigator as any).connection;

      const detector = new NetworkDetector();
      expect(detector.isSyncable()).toBe(true);
    });
  });

  describe('connectivity testing', () => {
    beforeEach(() => {
      global.fetch = jest.fn();
    });

    afterEach(() => {
      jest.restoreAllMocks();
    });

    it('should return false when offline', async () => {
      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });

      const detector = new NetworkDetector();
      const result = await detector.testConnectivity();

      expect(result).toBe(false);
      expect(fetch).not.toHaveBeenCalled();
    });

    it('should make health check when online', async () => {
      (global.fetch as jest.Mock).mockResolvedValue({ ok: true });

      const detector = new NetworkDetector();
      const result = await detector.testConnectivity();

      expect(result).toBe(true);
      expect(fetch).toHaveBeenCalledWith('/api/health', {
        method: 'HEAD',
        signal: expect.any(AbortSignal),
        cache: 'no-cache',
      });
    });

    it('should handle failed health checks', async () => {
      (global.fetch as jest.Mock).mockResolvedValue({ ok: false });

      const detector = new NetworkDetector();
      const result = await detector.testConnectivity();

      expect(result).toBe(false);
    });

    it('should handle network errors', async () => {
      (global.fetch as jest.Mock).mockRejectedValue(new Error('Network error'));
      const consoleSpy = jest.spyOn(console, 'warn').mockImplementation();

      const detector = new NetworkDetector();
      const result = await detector.testConnectivity();

      expect(result).toBe(false);
      expect(consoleSpy).toHaveBeenCalledWith('Connectivity test failed:', expect.any(Error));

      consoleSpy.mockRestore();
    });

    it('should respect timeout parameter', async () => {
      const warnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});
      const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
      (global.fetch as jest.Mock).mockImplementation(() => delay(200));

      const detector = new NetworkDetector();
      const result = await detector.testConnectivity(50);

      expect(result).toBe(false);
      expect(warnSpy).toHaveBeenCalled();
      warnSpy.mockRestore();
    });
  });
});

describe('useNetworkState React hook', () => {
  let originalConnection: any;

  beforeEach(() => {
    originalConnection = (navigator as any).connection;
    Object.defineProperty(navigator, 'onLine', { value: true, writable: true });
  });

  afterEach(() => {
    (navigator as any).connection = originalConnection;
  });

  it('should return initial network state', () => {
    const mockConnection = {
      type: 'cellular',
      effectiveType: '4g',
      downlink: 15,
      rtt: 30,
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    };
    (navigator as any).connection = mockConnection;

    const { result } = renderHook(() => useNetworkState());

    expect(result.current).toEqual({
      isOnline: true,
      connectionType: 'cellular',
      effectiveType: '4g',
      downlink: 15,
      rtt: 30,
    });
  });

  it('should update when network goes offline', () => {
    const { result } = renderHook(() => useNetworkState());

    act(() => {
      Object.defineProperty(navigator, 'onLine', { value: false, writable: true });
      simulateNetworkEvent('offline');
    });

    expect(result.current.isOnline).toBe(false);
  });

  it('should update when network comes back online', () => {
    Object.defineProperty(navigator, 'onLine', { value: false, writable: true });
    const { result } = renderHook(() => useNetworkState());

    act(() => {
      Object.defineProperty(navigator, 'onLine', { value: true, writable: true });
      simulateNetworkEvent('online');
    });

    expect(result.current.isOnline).toBe(true);
  });

  it('should update on connection property changes', () => {
    const mockConnection = {
      type: 'wifi',
      effectiveType: '4g',
      downlink: 10,
      rtt: 50,
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    };
    (navigator as any).connection = mockConnection;

    const { result } = renderHook(() => useNetworkState());

    act(() => {
      mockConnection.effectiveType = '3g';
      mockConnection.downlink = 5;
      simulateConnectionChange();
    });

    expect(result.current).toEqual({
      isOnline: true,
      connectionType: 'wifi',
      effectiveType: '3g',
      downlink: 5,
      rtt: 50,
    });
  });

  it('should work without connection API', () => {
    delete (navigator as any).connection;

    const { result } = renderHook(() => useNetworkState());

    expect(result.current).toEqual({ isOnline: true });
  });

  it('should clean up event listeners on unmount', () => {
    const removeEventListenerSpy = jest.spyOn(window, 'removeEventListener');

    const { unmount } = renderHook(() => useNetworkState());
    unmount();

    expect(removeEventListenerSpy).toHaveBeenCalledWith('online', expect.any(Function));
    expect(removeEventListenerSpy).toHaveBeenCalledWith('offline', expect.any(Function));

    removeEventListenerSpy.mockRestore();
  });

  it('should clean up connection listeners when available', () => {
    const mockConnection = {
      type: 'wifi',
      effectiveType: '4g',
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    };
    (navigator as any).connection = mockConnection;

    const { unmount } = renderHook(() => useNetworkState());
    unmount();

    expect(mockConnection.removeEventListener).toHaveBeenCalledWith('change', expect.any(Function));
  });
});
