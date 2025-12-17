/**
 * Hook to create and configure the Labour Service V2 Client
 */

import { useMemo } from 'react';
import { LabourServiceV2Client } from '@base/clients/labour_service';
import { useAuth } from '@clerk/clerk-react';

export function useLabourV2Client() {
  const { getToken } = useAuth();

  return useMemo(
    () =>
      new LabourServiceV2Client({
        baseUrl: import.meta.env.VITE_LABOUR_SERVICE_URL || '',
        getAccessToken: async () => {
          try {
            const token = await getToken();
            return token;
          } catch (error) {
            console.error('Failed to get access token:', error);
            return null;
          }
        },
      }),
    [getToken]
  );
}
