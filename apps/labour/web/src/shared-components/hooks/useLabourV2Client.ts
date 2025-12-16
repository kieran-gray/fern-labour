/**
 * Hook to create and configure the Labour Service V2 Client
 */

import { useMemo } from 'react';
import { useAuth } from '@clerk/clerk-react';
import { LabourServiceV2Client } from '@clients/labour_service_v2';

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
