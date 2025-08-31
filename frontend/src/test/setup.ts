import 'fake-indexeddb/auto';
import 'core-js/actual/structured-clone';

Object.defineProperty(navigator, 'onLine', {
  writable: true,
  value: true,
});

Object.defineProperty(navigator, 'storage', {
  writable: true,
  value: {
    estimate: jest.fn().mockResolvedValue({
      usage: 1000000,
      quota: 100000000,
    }),
  },
});

const originalAddEventListener = window.addEventListener.bind(window);
const originalRemoveEventListener = window.removeEventListener.bind(window);

window.addEventListener = ((event: any, handler: any, options?: any) => {
  if (event === 'online' || event === 'offline') {
    (window as any)[`${event}Handlers`] = (window as any)[`${event}Handlers`] || [];
    (window as any)[`${event}Handlers`].push(handler);
  }
  return originalAddEventListener(event, handler, options as any);
}) as any;

window.removeEventListener = ((event: any, handler: any, options?: any) => {
  if (event === 'online' || event === 'offline') {
    const key = `${event}Handlers`;
    const arr = ((window as any)[key] as any[]) || [];
    (window as any)[key] = arr.filter((h) => h !== handler);
  }
  return originalRemoveEventListener(event, handler, options as any);
}) as any;

(global as any).triggerNetworkEvent = (event: 'online' | 'offline') => {
  const handlers = (window as any)[`${event}Handlers`] || [];
  handlers.forEach((handler: any) => handler());
};

afterEach(() => {
  Object.defineProperty(navigator, 'onLine', {
    value: true,
    writable: true,
  });
});
