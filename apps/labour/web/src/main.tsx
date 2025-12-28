import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import '@mantine/dates/styles.css';
import '@mantine/charts/styles.css';
import '@mantine/carousel/styles.css';
import './styles.css';

import { StrictMode } from 'react';
import { ClerkProvider } from '@clerk/clerk-react';
import { QueryClientProvider } from '@tanstack/react-query';
import reactDom from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { MantineProvider } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import App from './App';
import { queryClient } from './config/index';
import { initializeQueryPersistence } from './offline/persistence/queryPersistence';
import { ProtectedApp } from './shared-components/ProtectedApp';
import { PWAUpdateHandler } from './shared-components/PWAUpdateHandler';
import { theme } from './theme';

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;
if (!PUBLISHABLE_KEY) {
  throw new Error('Missing Clerk Publishable Key');
}

async function initializeOfflineInfrastructure() {
  try {
    await initializeQueryPersistence(queryClient);
  } catch (error) {
    // Continue without offline features
  }
}

initializeOfflineInfrastructure();

// biome-ignore lint/style/noNonNullAssertion: We expect this element to always exist
reactDom.createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MantineProvider theme={theme}>
      <Notifications position="bottom-right" />
      <BrowserRouter basename="/">
        <ClerkProvider publishableKey={PUBLISHABLE_KEY} afterSignOutUrl="/">
          <QueryClientProvider client={queryClient}>
            <ProtectedApp>
              <PWAUpdateHandler />
              <App />
            </ProtectedApp>
          </QueryClientProvider>
        </ClerkProvider>
      </BrowserRouter>
    </MantineProvider>
  </StrictMode>
);
