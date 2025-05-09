import { StrictMode } from 'react';
import { QueryClientProvider } from '@tanstack/react-query';
import reactDom from 'react-dom/client';
import { AuthProvider } from 'react-oidc-context';
import { BrowserRouter } from 'react-router-dom';
import App from './App.tsx';
import { OpenAPI as ContactService } from './clients/contact_service';
import { OpenAPI as LabourService } from './clients/labour_service';
import { onSigninCallback, queryClient, userManager } from './config.ts';
import { ProtectedApp } from './shared-components/ProtectedApp.tsx';

LabourService.BASE = import.meta.env.VITE_LABOUR_SERVICE_URL;
ContactService.BASE = import.meta.env.VITE_CONTACT_SERVICE_URL;

// biome-ignore lint/style/noNonNullAssertion: We expect this element to always exist
reactDom.createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter basename="/">
      <AuthProvider userManager={userManager} onSigninCallback={onSigninCallback}>
        <QueryClientProvider client={queryClient}>
          <ProtectedApp>
            <App />
          </ProtectedApp>
        </QueryClientProvider>
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>
);
