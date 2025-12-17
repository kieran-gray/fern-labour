import { createContext, useContext, useEffect, useState } from 'react';
import { useApiAuth } from '@base/hooks/useApiAuth';

export enum AppMode {
  Subscriber = 'Subscriber',
  Birth = 'Birth',
}

interface ModeContextType {
  mode: AppMode | null;
  setMode: (mode: AppMode) => void;
}

const ModeContext = createContext<ModeContextType | undefined>(undefined);

export const ModeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useApiAuth();

  const userId = user?.sub || 'anonymous';

  const [mode, setMode] = useState<AppMode | null>(() => {
    const stored = localStorage.getItem(`${userId}:appMode`);
    return stored === AppMode.Birth || stored === AppMode.Subscriber ? stored : null;
  });

  useEffect(() => {
    localStorage.setItem(`${userId}:appMode`, mode || '');
  }, [mode, userId]);
  return <ModeContext.Provider value={{ mode, setMode }}>{children}</ModeContext.Provider>;
};

export const useMode = () => {
  const context = useContext(ModeContext);
  if (context === undefined) {
    throw new Error('useMode must be used within a ModeProvider');
  }
  return context;
};
