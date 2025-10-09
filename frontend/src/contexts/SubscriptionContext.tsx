import { createContext, useContext, useEffect, useState } from 'react';
import { useApiAuth } from '@base/shared-components/hooks/useApiAuth';

interface SubscriptionContextType {
  subscriptionId: string | null;
  setSubscriptionId: (subscriptionId: string) => void;
}

const SubscriptionContext = createContext<SubscriptionContextType | undefined>(undefined);

export const SubscriptionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useApiAuth();
  const userId = user?.profile.sub;
  const [subscriptionId, setSubscriptionId] = useState<string | null>(() => {
    return localStorage.getItem(`${userId}:subscriptionId`);
  });

  useEffect(() => {
    localStorage.setItem(`${userId}:subscriptionId`, subscriptionId || '');
  }, [subscriptionId]);

  return (
    <SubscriptionContext.Provider value={{ subscriptionId, setSubscriptionId }}>
      {children}
    </SubscriptionContext.Provider>
  );
};

export const useSubscription = () => {
  const context = useContext(SubscriptionContext);
  if (context === undefined) {
    throw new Error('useSubscription must be used within a SubscriptionProvider');
  }
  return context;
};
