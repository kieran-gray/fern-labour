/**
 * Initializes the sync manager with the authenticated client
 * Must be rendered inside the auth context
 */

import { useEffect } from 'react';
import { useLabourV2Client } from '@base/hooks/useLabourClient';
import { syncManager } from './syncManager';

export function SyncManagerInitializer() {
  const client = useLabourV2Client();

  useEffect(() => {
    syncManager.initialize(client);
  }, [client]);

  return null;
}
