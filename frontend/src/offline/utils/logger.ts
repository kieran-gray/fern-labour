// Lightweight logger for offline features. Disabled by default.
// Enable via:
//   localStorage.setItem('OFFLINE_DEBUG', '1')
// or temporarily in console:
//   window.__OFFLINE_DEBUG = true

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

function isEnabled(): boolean {
  if (typeof window !== 'undefined') {
    if ((window as any).__OFFLINE_DEBUG === true) {
      return true;
    }
    try {
      return window.localStorage?.getItem('OFFLINE_DEBUG') === '1';
    } catch {
      console.debug('pass');
    }
  }
  if (typeof process !== 'undefined' && (process as any).env) {
    return ((process as any).env.VITE_OFFLINE_DEBUG ?? (process as any).env.OFFLINE_DEBUG) === '1';
  }
  return false;
}

function log(level: LogLevel, tag: string, ...args: any[]) {
  if (!isEnabled()) {
    return;
  }
  const prefix = `[offline:${tag}]`;

  (console[level] || console.log).call(console, prefix, ...args);
}

export const offlineLogger = {
  debug: (tag: string, ...args: any[]) => log('debug', tag, ...args),
  info: (tag: string, ...args: any[]) => log('info', tag, ...args),
  warn: (tag: string, ...args: any[]) => log('warn', tag, ...args),
  error: (tag: string, ...args: any[]) => log('error', tag, ...args),
  setEnabled(enabled: boolean) {
    try {
      if (typeof window !== 'undefined') {
        window.localStorage?.setItem('OFFLINE_DEBUG', enabled ? '1' : '0');
      }
    } catch {
      console.debug('pass');
    }
    (window as any).__OFFLINE_DEBUG = enabled;
  },
  isEnabled,
};
