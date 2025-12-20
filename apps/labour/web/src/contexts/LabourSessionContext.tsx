import { createContext, useContext, useEffect, useState } from 'react';
import { useApiAuth } from '@base/hooks/useApiAuth';

export enum SessionRole {
  Mother = 'mother',
  Subscriber = 'subscriber',
  BirthPartner = 'birth-partner',
}

export enum AccessLevel {
  Full = 'full',
  Partner = 'partner',
  Viewer = 'viewer',
}

export interface LabourSessionState {
  labourId: string | null;
  subscriptionId: string | null;
  role: SessionRole | null;
  accessLevel: AccessLevel;
}

interface LabourSessionContextType extends LabourSessionState {
  setLabourId: (labourId: string | null) => void;
  setSubscriptionId: (subscriptionId: string | null) => void;
  setRole: (role: SessionRole | null) => void; // TODO
  startMotherSession: (labourId: string) => void;
  startSubscriberSession: (subscriptionId: string) => void;
  clearSession: () => void;
}

const LabourSessionContext = createContext<LabourSessionContextType | undefined>(undefined);

function getAccessLevel(role: SessionRole | null): AccessLevel {
  switch (role) {
    case SessionRole.Mother:
      return AccessLevel.Full;
    case SessionRole.BirthPartner:
      return AccessLevel.Partner;
    case SessionRole.Subscriber:
      return AccessLevel.Viewer;
    default:
      return AccessLevel.Viewer;
  }
}

export const LabourSessionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useApiAuth();
  const userId = user?.sub;

  const [labourId, setLabourIdState] = useState<string | null>(() => {
    return localStorage.getItem(`${userId}:labourId`) || null;
  });

  const [subscriptionId, setSubscriptionIdState] = useState<string | null>(() => {
    return localStorage.getItem(`${userId}:subscriptionId`) || null;
  });

  const [role, setRoleState] = useState<SessionRole | null>(() => {
    const stored = localStorage.getItem(`${userId}:sessionRole`);
    if (stored && Object.values(SessionRole).includes(stored as SessionRole)) {
      return stored as SessionRole;
    }
    return null;
  });

  useEffect(() => {
    if (userId) {
      localStorage.setItem(`${userId}:labourId`, labourId || '');
    }
  }, [labourId, userId]);

  useEffect(() => {
    if (userId) {
      localStorage.setItem(`${userId}:subscriptionId`, subscriptionId || '');
    }
  }, [subscriptionId, userId]);

  useEffect(() => {
    if (userId) {
      localStorage.setItem(`${userId}:sessionRole`, role || '');
    }
  }, [role, userId]);

  useEffect(() => {
    if (!role) {
      if (labourId && !subscriptionId) {
        setRoleState(SessionRole.Mother);
      } else if (subscriptionId && !labourId) {
        setRoleState(SessionRole.Subscriber);
      }
    }
  }, [labourId, subscriptionId, role]);

  const setLabourId = (id: string | null) => {
    setLabourIdState(id);
  };

  const setSubscriptionId = (id: string | null) => {
    setSubscriptionIdState(id);
  };

  const setRole = (newRole: SessionRole | null) => {
    setRoleState(newRole);
  };

  const startMotherSession = (id: string) => {
    setLabourIdState(id);
    setSubscriptionIdState(null);
    setRoleState(SessionRole.Mother);
  };

  const startSubscriberSession = (id: string) => {
    setSubscriptionIdState(id);
    setLabourIdState(null);
    setRoleState(SessionRole.Subscriber);
  };

  const clearSession = () => {
    setLabourIdState(null);
    setSubscriptionIdState(null);
    setRoleState(null);
  };

  const accessLevel = getAccessLevel(role);

  const value: LabourSessionContextType = {
    labourId,
    subscriptionId,
    role,
    accessLevel,
    setLabourId,
    setSubscriptionId,
    setRole,
    startMotherSession,
    startSubscriberSession,
    clearSession,
  };

  return <LabourSessionContext.Provider value={value}>{children}</LabourSessionContext.Provider>;
};

export const useLabourSession = () => {
  const context = useContext(LabourSessionContext);
  if (context === undefined) {
    throw new Error('useLabourSession must be used within a LabourSessionProvider');
  }
  return context;
};
