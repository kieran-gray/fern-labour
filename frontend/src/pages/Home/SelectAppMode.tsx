import { createContext, useContext, useEffect, useState } from 'react';
import { useApiAuth } from '@base/shared-components/hooks/useApiAuth';
import { useNavigate } from 'react-router-dom';
import { Badge, Button, Card, Text, ThemeIcon, Title } from '@mantine/core';
import { IconBabyCarriage, IconHeart, IconArrowRight, IconUsers, IconBell, IconCalendar } from '@tabler/icons-react';
import classes from './SelectAppMode.module.css';
import baseClasses from '@shared/shared-styles.module.css';

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
  const userId = user?.profile.sub;
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

  const handleModeSelect = (selectedMode: AppMode) => {
    setMode(selectedMode);
    navigate('/');
  };

  return (
    <div className={baseClasses.flexPageColumn}>
        {/* Header Section */}
        <div className={classes.header}>
          <Title className={classes.mainTitle} ta="center" mb="md">
            Welcome to Fern Labour
          </Title>
          <Text size="lg" className={classes.mainDescription} ta="center" maw={600} mx="auto">
                  We’re so glad you’re here! Whether you're tracking your own labour journey or
                  following and supporting someone special, you’re in the right place.
          </Text>
        </div>

        {/* Mode Selection */}
        <div className={classes.modeSelection}>
          <Title order={3} className={classes.mainCTA} ta="center" mb="xl">
            Choose your journey
          </Title>

          <div className={classes.cardsGrid}>
            {/* Birth Mode Card */}
            <Card
              className={classes.modeCard}
              onClick={() => handleModeSelect(AppMode.Birth)}
              withBorder
              radius="xl"
              p="xl"
            >
              <div className={classes.cardContent}>
                <div className={classes.cardHeader}>
                  <ThemeIcon
                    className={classes.primaryIcon}
                    size={60}
                    radius="xl"
                    variant="light"
                    color="pink"
                  >
                    <IconBabyCarriage size={32} />
                  </ThemeIcon>
                  <Badge className={classes.primaryBadge} variant="light" color="pink" size="sm">
                    For expecting parents
                  </Badge>
                </div>

                <Title order={2} className={classes.cardTitle} mb="xs">
                  Birth Mode
                </Title>
                
                <Text className={classes.cardDescription} mb="lg">
                  Track your labour journey with precision and share meaningful updates with your support network
                </Text>

                <div className={classes.featureList}>
                  <div className={classes.feature}>
                    <IconCalendar size={16} className={classes.featureIcon} />
                    <Text size="sm">Plan and track contractions</Text>
                  </div>
                  <div className={classes.feature}>
                    <IconBell size={16} className={classes.featureIcon} />
                    <Text size="sm">Share real-time updates</Text>
                  </div>
                  <div className={classes.feature}>
                    <IconUsers size={16} className={classes.featureIcon} />
                    <Text size="sm">Invite family & friends</Text>
                  </div>
                </div>

                <Button
                  fullWidth
                  size="md"
                  radius="lg"
                  variant="filled"
                  color="pink"
                  rightSection={<IconArrowRight size={18} />}
                >
                  Start Your Journey
                </Button>
              </div>
            </Card>

            {/* Subscriber Mode Card */}
            <Card
              className={classes.modeCard}
              onClick={() => handleModeSelect(AppMode.Subscriber)}
              withBorder
              radius="xl"
              p="xl"
            >
              <div className={classes.cardContent}>
                <div className={classes.cardHeader}>
                  <ThemeIcon
                    className={classes.supportIcon}
                    size={60}
                    radius="xl"
                    variant="light"
                    color="blue"
                  >
                    <IconHeart size={32} />
                  </ThemeIcon>
                  <Badge className={classes.supportBadge} variant="light" color="blue" size="sm">
                    For support network
                  </Badge>
                </div>

                <Title order={2} className={classes.cardTitle} mb="xs">
                  Support Mode
                </Title>
                
                <Text className={classes.cardDescription} mb="lg">
                  Stay connected and provide loving support to someone special during their labour journey
                </Text>

                <div className={classes.featureList}>
                  <div className={classes.feature}>
                    <IconBell size={16} className={classes.featureIcon} />
                    <Text size="sm">Receive live notifications</Text>
                  </div>
                  <div className={classes.feature}>
                    <IconUsers size={16} className={classes.featureIcon} />
                    <Text size="sm">Join their support circle</Text>
                  </div>
                </div>

                <Button
                  fullWidth
                  size="md"
                  variant="outline"
                  radius="lg"
                  color="blue"
                  rightSection={<IconArrowRight size={18} />}
                >
                  Join & Support
                </Button>
              </div>
            </Card>
          </div>
        </div>

        {/* Footer Note */}
        <div className={classes.footer}>
          <Text size="sm" ta="center">
            💡 You can switch between modes anytime in your profile settings
          </Text>
        </div>
    </div>
  );
}
