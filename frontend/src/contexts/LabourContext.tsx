import { createContext, useContext, useEffect, useState } from 'react';
import { useApiAuth } from '@base/shared-components/hooks/useApiAuth';

interface LabourContextType {
  labourId: string | null;
  setLabourId: (labourId: string | null) => void;
}

export const LabourContext = createContext<LabourContextType | undefined>(undefined);

export const useLabour = () => {
  const context = useContext(LabourContext);
  if (context === undefined) {
    throw new Error('useLabour must be used within a LabourProvider');
  }
  return context;
};

export const LabourProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useApiAuth();
  const userId = user?.profile.sub;
  const [labourId, setLabourId] = useState<string | null>(() => {
    return localStorage.getItem(`${userId}:labourId`);
  });

  useEffect(() => {
    localStorage.setItem(`${userId}:labourId`, labourId || '');
  }, [labourId]);

  return (
    <LabourContext.Provider value={{ labourId, setLabourId }}>{children}</LabourContext.Provider>
  );
};
