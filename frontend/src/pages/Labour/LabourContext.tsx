import { createContext, useContext } from 'react';

export const LabourContext = createContext<string | null>(null);

export const useLabour = () => {
  const context = useContext(LabourContext);
  if (context === null) {
    throw new Error('useLabour must be used within a LabourProvider');
  }
  return context;
};

export const LabourProvider = ({
  children,
  labourId,
}: {
  children: React.ReactNode;
  labourId: string;
}) => {
  return <LabourContext.Provider value={labourId}>{children}</LabourContext.Provider>;
};
