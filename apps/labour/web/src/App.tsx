import { ModeProvider } from './contexts/AppModeContext';
import { LabourSessionProvider } from './contexts/LabourSessionContext';
import { Router } from './Router';

export default function App() {
  return (
    <LabourSessionProvider>
      <ModeProvider>
        <Router />
      </ModeProvider>
    </LabourSessionProvider>

  );
}
