import { useNavigate } from 'react-router-dom';
import { Button, Image, Mark, Text, Title } from '@mantine/core';
import { AppShell } from '../../shared-components/AppShell';
import image from './thanks.svg';
import baseClasses from '../../shared-components/shared-styles.module.css';
import classes from './CompletedLabour.module.css';

export const CompletedLabourContainer: React.FC = () => {
  const navigate = useNavigate();
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <div className={baseClasses.content}>
            <Title order={1} visibleFrom="sm">
              Thank you for choosing Fern Labour
            </Title>
            <Title order={2} hiddenFrom="sm">
              Thank you for choosing Fern Labour
            </Title>
            <div className={baseClasses.flexRow} style={{ flexWrap: 'nowrap' }}>
              <div className={baseClasses.flexColumn}>
                <Text c="var(--mantine-color-gray-7)" mt="md" size="md">
                  <Mark color="transparent" fw={700} fz="lg">
                    You did it!
                  </Mark>{' '}
                  Bringing new life into the world is an incredible journey, and we are so proud of
                  you. Take a deep breath, soak in this beautiful moment, and know that you are
                  amazing.
                </Text>
                <div className={classes.imageFlexRow}>
                  <Image src={image} className={classes.smallImage} />
                </div>
                <Text c="var(--mantine-color-gray-7)" mt="sm" size="md">
                  We're so grateful for you for choosing to use our platform. If you'd like to, we'd
                  love to know what you liked or what you would like to see done differently through
                  the contact form below.
                </Text>
                <Button
                  size="md"
                  mt={20}
                  color="var(--mantine-color-pink-4)"
                  radius="xl"
                  variant="light"
                  onClick={() => navigate('/contact')}
                >
                  Contact us
                </Button>
              </div>
              <Image
                src={image}
                className={classes.image}
                style={{ flexGrow: 1, marginLeft: '20px' }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export const CompletedLabourPage: React.FC = () => {
  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <CompletedLabourContainer />
      </div>
    </AppShell>
  );
};
