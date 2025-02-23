import { createContext, useContext, useEffect, useState } from 'react';
import { IconInfoCircle } from '@tabler/icons-react';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Button, Text, Title } from '@mantine/core';
import { ContainerHeader } from '../../shared-components/ContainerHeader/ContainerHeader';
import baseClasses from '../../shared-components/shared-styles.module.css';
import classes from './SelectAppMode.module.css';

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
  const auth = useAuth();
  const userId = auth.user?.profile.sub;
  const [mode, setMode] = useState<AppMode | null>(() => {
    const stored = localStorage.getItem(`${userId}:appMode`);
    return stored === AppMode.Birth || stored === AppMode.Subscriber ? stored : null;
  });

  useEffect(() => {
    localStorage.setItem(`${userId}:appMode`, mode || '');
  }, [mode]);

  return <ModeContext.Provider value={{ mode, setMode }}>{children}</ModeContext.Provider>;
};

export const useMode = () => {
  const context = useContext(ModeContext);
  if (context === undefined) {
    throw new Error('useMode must be used within a ModeProvider');
  }
  return context;
};

export function SelectAppMode() {
  const navigate = useNavigate();
  const { setMode } = useMode();

  return (
    <div className={baseClasses.flexPageColumn}>
      <div className={baseClasses.root} style={{ marginTop: '4vh' }}>
        <ContainerHeader title="Welcome" />
        <div className={baseClasses.body}>
          <div className={baseClasses.inner}>
            <div className={classes.content}>
              <div className={classes.flexRow}>
                <Title className={classes.title} ta="center">
                  Welcome to Fern Labour
                </Title>
                <Text c="var(--mantine-color-gray-7)" mt="md" ta="center">
                  We’re so glad you’re here! Whether you're tracking your own labour journey or
                  following and supporting someone special, you’re in the right place.
                </Text>
              </div>
              <div className={classes.selectRow}>
                <Title order={4}>Choose your experience to get started:</Title>
              </div>
              <div className={classes.selectRow}>
                <Button
                  h={200}
                  maw={400}
                  radius="xl"
                  variant="light"
                  onClick={() => {
                    setMode(AppMode.Birth);
                    navigate('/');
                  }}
                  classNames={{ label: classes.buttonLabel }}
                >
                  👶 Birth Mode – Plan and track your labour, log contractions, and share updates.
                </Button>
                <Title order={4} mt={10} mb={10}>
                  Or
                </Title>
                <Button
                  h={200}
                  maw={400}
                  radius="xl"
                  variant="light"
                  onClick={() => {
                    setMode(AppMode.Subscriber);
                    navigate('/');
                  }}
                  classNames={{ label: classes.buttonLabel }}
                >
                  ❤️ Subscriber Mode – Stay connected and support a loved one through their journey.
                </Button>
              </div>
              <div className={classes.selectRow}>
                <div
                  className={baseClasses.importantText}
                  style={{ display: 'flex', justifyContent: 'center' }}
                >
                  <IconInfoCircle style={{ alignSelf: 'center', marginRight: '10px' }} />
                  You can change modes at any time in the app menu.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
