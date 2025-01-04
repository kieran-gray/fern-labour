import { QueryClientProvider } from '@tanstack/react-query';
import { StrictMode } from 'react';
import reactDom from 'react-dom/client';
import { AuthProvider } from 'react-oidc-context';
import App from './App.tsx';
import { ProtectedApp } from './shared-components/ProtectedApp.tsx';
import { onSigninCallback, queryClient, userManager } from './config.ts';

import { OpenAPI } from "./client"

OpenAPI.BASE = import.meta.env.VITE_API_URL

// biome-ignore lint/style/noNonNullAssertion: We expect this element to always exist
reactDom.createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <AuthProvider userManager={userManager} onSigninCallback={onSigninCallback}>
        <QueryClientProvider client={queryClient}>
          <ProtectedApp>
            <App />
          </ProtectedApp>
        </QueryClientProvider>
      </AuthProvider>
  </StrictMode>
);
