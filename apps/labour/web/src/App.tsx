import { ModeProvider } from './contexts/AppModeContext';
import { LabourProvider } from './contexts/LabourContext';
import { Router } from './Router';

export default function App() {
  return (
    <ModeProvider>
      <LabourProvider>
        <Router />
      </LabourProvider>
    </ModeProvider>
  );
}
