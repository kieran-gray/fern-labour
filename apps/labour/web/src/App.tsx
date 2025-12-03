import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import '@mantine/dates/styles.css';
import '@mantine/charts/styles.css';
import '@mantine/carousel/styles.css';
import './styles.css';

import { MantineProvider } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import { ModeProvider } from './contexts/AppModeContext';
import { LabourProvider } from './contexts/LabourContext';
import { Router } from './Router';
import { theme } from './theme';

export default function App() {
  return (
    <MantineProvider theme={theme}>
      <ModeProvider>
        <LabourProvider>
          <Notifications position="bottom-right" />
          <Router />
        </LabourProvider>
      </ModeProvider>
    </MantineProvider>
  );
}
