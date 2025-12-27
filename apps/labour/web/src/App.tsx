import { LabourSessionProvider } from './contexts/LabourSessionContext';
import { WebSocketProvider } from './contexts/WebsocketContext';
import { useWebSocketInvalidation } from './hooks/useWebSocketInvalidation';
import { Router } from './Router';

function AppWithWebSocket() {
  useWebSocketInvalidation();
  return <Router />;
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
