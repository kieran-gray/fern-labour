/**
 * Hook to handle websocket connection to the backend
 */
import { useEffect } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useAuth } from '@clerk/clerk-react';
import { useLabourSession } from '@base/contexts';

export function useWebsocketConnection() {
    const queryClient = useQueryClient();
    const { getToken } = useAuth();
    const { labourId } = useLabourSession();

    useEffect(() => {
        if (!labourId) {
            return;
        } 

        let websocket: WebSocket | null = null;

        const connect = async () => {
            const token = await getToken();
            const wsUrl = import.meta.env.VITE_LABOUR_SERVICE_WEBSOCKET || '';

            websocket = new WebSocket(`${wsUrl}${labourId}`, `base64url.bearer.authorization.fernlabour.com.${token}`);

            websocket.onopen = () => {
                console.log("connected");
            };

            websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log(data)
                const queryKey = [...data.entity, data.id].filter(Boolean);
                queryClient.invalidateQueries({ queryKey });
            };
        };

        connect();

        return () => {
            websocket?.close();
        };
    }, [labourId, getToken, queryClient]);
}
