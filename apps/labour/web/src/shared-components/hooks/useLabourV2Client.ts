/**
 * Hook to create and configure the Labour Service V2 Client
 */

import { useMemo } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { LabourServiceV2Client } from '@clients/labour_service_v2';

export function useLabourV2Client() {
  const { getAccessTokenSilently } = useAuth0();

  return useMemo(
    () =>
      new LabourServiceV2Client({
        baseUrl: import.meta.env.VITE_LABOUR_SERVICE_URL || '',
        getAccessToken: async () => {
          try {
            const token = await getAccessTokenSilently();
            return token;
          } catch (error) {
            console.error('Failed to get access token:', error);
            return null;
          }
        },
      }),
    [getAccessTokenSilently]
  );
}
