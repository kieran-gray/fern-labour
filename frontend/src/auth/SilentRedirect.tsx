import { useEffect } from 'react';
import { userManager } from '../config';

export function SilentRedirect() {
  useEffect(() => {
    userManager.signinSilentCallback().catch(() => {
      // Intentionally ignore; parent window handles fallback
    });
  }, []);
  return null;
}
