import { StrictMode } from 'react';
import { QueryClientProvider } from '@tanstack/react-query';
import reactDom from 'react-dom/client';
import { AuthProvider } from 'react-oidc-context';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { OpenAPI as ContactService } from './clients/contact_service';
import { OpenAPI as LabourService } from './clients/labour_service';
import { onSigninCallback, queryClient, userManager } from './config/index';
import { SyncEngineProvider } from './offline/hooks/SyncEngineProvider';
import { GuestModeProvider } from './offline/hooks/useGuestMode';
import { initializeQueryPersistence } from './offline/persistence/queryPersistence';
import { initializeDatabase } from './offline/storage/database';
import { ProtectedApp } from './shared-components/ProtectedApp';
import { PWAUpdateHandler } from './shared-components/PWAUpdateHandler';

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
    <BrowserRouter basename="/">
      <AuthProvider userManager={userManager} onSigninCallback={onSigninCallback}>
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
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);
