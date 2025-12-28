import { LabourSessionProvider } from './contexts/LabourSessionContext';
import { WebSocketProvider } from './contexts/WebsocketContext';
import { useWebSocketInvalidation } from './hooks/useWebSocketInvalidation';
import { SyncManagerInitializer } from './offline/SyncManagerInitializer';
import { Router } from './Router';

function AppWithWebSocket() {
  useWebSocketInvalidation();
  return (
    <>
      <SyncManagerInitializer />
      <Router />
    </>
  );
}

export default function App() {
  return (
    <LabourSessionProvider>
      <WebSocketProvider>
        <AppWithWebSocket />
      </WebSocketProvider>
    </LabourSessionProvider>
  );
}
