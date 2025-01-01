import { QueryClientProvider } from '@tanstack/react-query';
import React from 'react';
import reactDom from 'react-dom/client';
import { AuthProvider } from 'react-oidc-context';
import App from './App.tsx';
import { ProtectedApp } from './components/ProtectedApp.tsx';
import { onSigninCallback, queryClient, userManager } from './config.ts';

// biome-ignore lint/style/noNonNullAssertion: We expect this element to always exist
reactDom.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
      <AuthProvider userManager={userManager} onSigninCallback={onSigninCallback}>
        <QueryClientProvider client={queryClient}>
          <ProtectedApp>
            <App />
          </ProtectedApp>
        </QueryClientProvider>
      </AuthProvider>
  </React.StrictMode>
);
