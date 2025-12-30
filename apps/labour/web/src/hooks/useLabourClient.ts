/**
 * Hook to create and configure the Labour Service Client
 */

import { useMemo } from 'react';
import { LabourServiceClient } from '@base/clients/labour_service';
import { useWebSocket } from '@base/contexts/WebsocketContext';
import { useAuth } from '@clerk/clerk-react';

export function useLabourClient() {
  const { getToken } = useAuth();
  const websocket = useWebSocket();

  return useMemo(
    () =>
      new LabourServiceClient({
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
        websocket: {
          isConnected: websocket.isConnected,
          sendMessage: websocket.sendMessage,
        },
      }),
    [getToken, websocket.isConnected, websocket.sendMessage]
  );
}
