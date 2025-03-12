import { IconArrowUp } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import { Button, Image, Text, Title } from '@mantine/core';
import image from './ShareMore.svg';
import baseClasses from '../shared-styles.module.css';
import classes from './PayWall.module.css';

export const PayWall = () => {
  const navigate = useNavigate();
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <div className={baseClasses.flexColumn}>
            <Title order={1} visibleFrom="sm">
              Ready to Share More?
            </Title>
            <Title order={2} hiddenFrom="sm">
              Ready to Share More?
            </Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              This feature is available exclusively to members on paid plans.
              <br />
              Upgrade your birth experience to unlock unlimited sharing capabilities and additional
              tools to keep your loved ones connected throughout your journey.
            </Text>
            <div className={classes.imageFlexRow} style={{ marginTop: '20px' }}>
              <Image src={image} className={classes.smallImage} />
            </div>
            <Button
              leftSection={<IconArrowUp size={18} stroke={1.5} />}
              variant="filled"
              radius="xl"
              size="lg"
              onClick={() => navigate('/onboarding?step=pay')}
            >
              Upgrade now
            </Button>
          </div>
          <Image src={image} className={classes.image} />
        </div>
      </div>
    </div>
  );
};
