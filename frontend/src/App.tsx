import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import '@mantine/dates/styles.css';
import '@mantine/charts/styles.css';
import './styles.css';

import { MantineProvider } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import { ModeProvider } from './pages/Home/SelectAppMode';
import { Router } from './Router';
import { theme } from './theme';

export default function App() {
  return (
    <MantineProvider theme={theme}>
      <ModeProvider>
        <Notifications position="bottom-right" />
        <Router />
      </ModeProvider>
    </MantineProvider>
  );
}
