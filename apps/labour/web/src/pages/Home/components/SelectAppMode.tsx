import { AppMode, useLabourSession } from '@base/contexts/LabourSessionContext';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { IconBabyCarriage, IconBulb, IconHeart } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import { Badge, Text, ThemeIcon, Title } from '@mantine/core';
import classes from './SelectAppMode.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export function SelectAppMode() {
  const navigate = useNavigate();
  const { setMode } = useLabourSession();

  const handleModeSelect = (selectedMode: AppMode) => {
    setMode(selectedMode);
    navigate('/');
  };

  return (
    <div className={baseClasses.flexPageColumn}>
      {/* Warm Hero Card with options inside */}
      <div className={baseClasses.root} style={{ width: '100%' }}>
        <div className={`${baseClasses.body} ${classes.heroCard}`}>
          <div className={baseClasses.inner}>
            <div className={classes.heroContent}>
              <div>
                <div className={classes.kicker}>Welcome</div>
                <Title order={2}>How would you like to start?</Title>
                <ResponsiveDescription
                  description={
                    <>
                      Whether you're tracking your own labour journey or following and supporting
                      someone special, you're in the right place.
                    </>
                  }
                  marginTop={10}
                />
              </div>

              <div className={classes.optionsRow}>
                {/* Expecting tile */}
                <div
                  className={classes.modeTile}
                  role="button"
                  tabIndex={0}
                  onClick={() => handleModeSelect(AppMode.Birth)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      handleModeSelect(AppMode.Birth);
                    }
                  }}
                  aria-describedby="expecting-sub"
                >
                  <div className={classes.tileHeader}>
                    <ThemeIcon
                      className={classes.primaryIcon}
                      size={56}
                      radius="xl"
                      variant="light"
                      color="pink"
                    >
                      <IconBabyCarriage size={30} />
                    </ThemeIcon>
                    <Badge className={classes.primaryBadge} variant="light" color="pink" size="sm">
                      Expecting
                    </Badge>
                  </div>
                  <Title order={3} className={classes.tileTitle}>
                    I'm expecting
                  </Title>
                  <Text size="sm" className={classes.tileSub} id="expecting-sub">
                    Track contractions, invite family & friends, share updates.
                  </Text>
                </div>

                {/* Supporting tile */}
                <div
                  className={classes.modeTile}
                  role="button"
                  tabIndex={0}
                  onClick={() => handleModeSelect(AppMode.Subscriber)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      handleModeSelect(AppMode.Subscriber);
                    }
                  }}
                  aria-describedby="supporting-sub"
                >
                  <div className={classes.tileHeader}>
                    <ThemeIcon
                      className={classes.supportIcon}
                      size={56}
                      radius="xl"
                      variant="light"
                      color="blue"
                    >
                      <IconHeart size={30} />
                    </ThemeIcon>
                    <Badge className={classes.supportBadge} variant="light" color="blue" size="sm">
                      Supporting
                    </Badge>
                  </div>
                  <Title order={3} className={classes.tileTitle}>
                    I'm supporting
                  </Title>
                  <Text size="sm" className={classes.tileSub} id="supporting-sub">
                    Get timely updates and know how to help.
                  </Text>
                </div>
              </div>

              <div className={classes.trustRow}>
                <span className={classes.trustItem}>
                  <IconBulb className={classes.trustIcon} />
                  <span className={classes.trustText}>
                    You can switch between modes anytime in the app settings
                  </span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
