import { useMemo } from 'react';
import { ContactServiceClient } from '@clients/contact_service';

export function useContactClient() {
  return useMemo(
    () =>
      new ContactServiceClient({
        baseUrl: import.meta.env.VITE_CONTACT_SERVICE_URL || '',
      }),
    []
  );
}
