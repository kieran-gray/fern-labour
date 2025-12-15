import '@mantine/core/styles.css';
import '@mantine/notifications/styles.css';
import '@mantine/dates/styles.css';
import '@mantine/charts/styles.css';
import '@mantine/carousel/styles.css';
import './styles.css';

import { StrictMode } from 'react';
import { Auth0Provider } from '@auth0/auth0-react';
import { QueryClientProvider } from '@tanstack/react-query';
import reactDom from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { MantineProvider } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import App from './App';
import { OpenAPI as ContactService } from './clients/contact_service';
import { OpenAPI as LabourService } from './clients/labour_service';
import { auth0Config, queryClient } from './config/index';
import { SyncEngineProvider } from './offline/hooks/SyncEngineProvider';
import { GuestModeProvider } from './offline/hooks/useGuestMode';
import { initializeQueryPersistence } from './offline/persistence/queryPersistence';
import { initializeDatabase } from './offline/storage/database';
import { ProtectedApp } from './shared-components/ProtectedApp';
import { PWAUpdateHandler } from './shared-components/PWAUpdateHandler';
import { theme } from './theme';

LabourService.BASE = import.meta.env.VITE_LABOUR_SERVICE_URL;
ContactService.BASE = import.meta.env.VITE_CONTACT_SERVICE_URL;

async function initializeOfflineInfrastructure() {
  try {
    await initializeDatabase();
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
        <Auth0Provider
          domain={auth0Config.domain}
          clientId={auth0Config.clientId}
          authorizationParams={{
            redirect_uri: auth0Config.redirectUri,
            audience: auth0Config.audience,
            scope: 'openid profile email offline_access',
          }}
          useRefreshTokens
          cacheLocation="localstorage"
        >
          <QueryClientProvider client={queryClient}>
            <SyncEngineProvider>
              <GuestModeProvider>
                <ProtectedApp>
                  <PWAUpdateHandler />
                  <App />
                </ProtectedApp>
              </GuestModeProvider>
            </SyncEngineProvider>
          </QueryClientProvider>
        </Auth0Provider>
      </BrowserRouter>
    </MantineProvider>
  </StrictMode>
);
