'use client';

import { ReactNode, useMemo, useState } from 'react';
import {
  IconCalendar,
  IconCurrencyPound,
  IconHourglass,
  IconLink,
  IconLock,
  IconMail,
  IconMessage,
  IconSend,
  IconStopwatch,
  IconUserPlus,
  IconUsers,
} from '@tabler/icons-react';
import { motion } from 'motion/react';
import { Box, Card, Container, Flex, Grid, SegmentedControl, Stack, Text } from '@mantine/core';
import { JumboTitle } from '../JumboTitle/JumboTitle';
import classes from './FeaturesMotion.module.css';
import { FeaturesDemo } from '../FeaturesCarousel/FeaturesCarousel';

type Feature = {
  icon: ReactNode;
  title: string;
  description: ReactNode;
};

const MUM_FEATURES: Feature[] = [
  {
    icon: <IconUserPlus color="var(--mantine-color-pink-6)" />,
    title: 'Sign Up',
    description: 'Create your free Fern Labour account and get ready to share your journey.',
  },
  {
    icon: <IconCalendar color="var(--mantine-color-pink-6)" />,
    title: 'Plan Your Labour',
    description: 'Set your due date and share a few preferences for a personalised experience.',
  },
  {
    icon: <IconSend color="var(--mantine-color-pink-6)" />,
    title: 'Invite Loved Ones',
    description: 'Send invites via email, link, or QR code so they can follow your progress.',
  },
  {
    icon: <IconUsers color="var(--mantine-color-pink-6)" />,
    title: 'Accept Subscribers',
    description: 'Approve or remove people at any time, you’re in control of who’s included.',
  },
  {
    icon: <IconMessage color="var(--mantine-color-pink-6)" />,
    title: 'Share Updates',
    description:
      'Keep your loved ones informed before and during your labour with one-tap status updates.',
  },
  {
    icon: <IconStopwatch color="var(--mantine-color-pink-6)" />,
    title: 'Track Contractions',
    description: 'Monitor your contractions and get alerts when it’s time to go to the hospital.',
  },
] as const;

const SUBSCRIBER_FEATURES: Feature[] = [
  {
    icon: <IconMail color="var(--mantine-color-pink-6)" />,
    title: 'Receive an Invite',
    description: 'A loved one shares a private link with you via email, text, or QR code.',
  },
  {
    icon: <IconLink color="var(--mantine-color-pink-6)" />,
    title: 'Follow the Invite Link',
    description: 'Open the invite to begin. The link contains your subscription token.',
  },
  {
    icon: <IconUserPlus color="var(--mantine-color-pink-6)" />,
    title: 'Sign Up',
    description: 'Create your free Fern Labour account to stay connected.',
  },
  {
    icon: <IconLock color="var(--mantine-color-pink-6)" />,
    title: 'Request Access',
    description: 'Your token is used to request access from the expectant mother.',
  },
  {
    icon: <IconHourglass color="var(--mantine-color-pink-6)" />,
    title: 'Wait for Approval',
    description: 'Once approved, you’ll be able to follow their labour journey.',
  },
  {
    icon: <IconCurrencyPound color="var(--mantine-color-pink-6)" />,
    title: 'Upgrade for Notifications',
    description: 'Pay £2.50 to receive real-time updates by SMS or WhatsApp.',
  },
] as const;

const FeatureCell = ({
  icon,
  title,
  description,
  index = 1,
  iconSize,
}: Feature & {
  index?: number;
  iconSize?: number;
}) => (
  <motion.div
    initial={{ opacity: 0.0, y: 40 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5, delay: 0.1 * index, ease: 'easeInOut' }}
    viewport={{ once: true }}
    style={{ height: '100%' }}
  >
    <motion.div
      whileHover={{ scale: 1.01, boxShadow: 'var(--mantine-shadow-md)' }}
      transition={{ type: 'spring' }}
      style={{
        borderRadius: 'var(--mantine-radius-lg)',
        height: '100%',
      }}
    >
      <Card radius="lg" p="xl" className={classes.cell} h="100%">
        <Stack gap="xs">
          <Flex w={iconSize} h={iconSize} justify="center" align="center">
            {icon}
          </Flex>
          <Box>
            <Text fz="xl" className={classes.cellTitle}>
              Step {index + 1}: {title}
            </Text>
            <Text fz="md" c="var(--mantine-color-gray-8)">
              {description}
            </Text>
          </Box>
        </Stack>
      </Card>
    </motion.div>
  </motion.div>
);

type Feature02Props = {
  title?: string;
  mum_features?: Feature[];
  subscriber_features?: Feature[];
  iconSize?: number;
};

export const Feature02 = ({
  title = 'How It Works',
  mum_features = MUM_FEATURES,
  subscriber_features = SUBSCRIBER_FEATURES,
  iconSize = 20,
}: Feature02Props) => {
  const [mode, setMode] = useState('mum');

  const featuresToRender = useMemo(() => {
    return mode === 'mum' ? mum_features : subscriber_features;
  }, [mode, mum_features, subscriber_features]);

  const controlProps = {
    fullWidth: true,
    radius: 'xl',
    mt: 'xl',
    mb: 'xl',
    color: 'var(--mantine-color-pink-4)',
  };

  return (
    <Container
      py="calc(var(--mantine-spacing-lg) * 3)"
      px="15px"
      fluid
    >
      <Container size="lg" px={0} style={{ position: 'relative' }} id="#features">
        <JumboTitle order={2} fz="md" ta="center" style={{ textWrap: 'balance' }}>
          {title}
        </JumboTitle>
        <FeaturesDemo />
        <SegmentedControl
          size="xl"
          visibleFrom="sm"
          value={mode}
          onChange={setMode}
          {...controlProps}
          data={[
            { value: 'mum', label: 'For Mums' },
            { value: 'subscriber', label: 'For Loved Ones' },
          ]}
        />
        <SegmentedControl
          size="md"
          hiddenFrom="sm"
          value={mode}
          onChange={setMode}
          {...controlProps}
          data={[
            { value: 'mum', label: 'For Mums' },
            { value: 'subscriber', label: 'For Loved Ones' },
          ]}
        />
      </Container>
      <Container size="lg" p={0} mt="xl">
        <Grid gutter="lg">
          {featuresToRender.map((feature, index) => (
            <Grid.Col key={`${feature.title}-${mode}`} span={{ base: 12, xs: 6, md: 4 }} mih="100%">
              <FeatureCell
                key={feature.title}
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
                index={index}
                iconSize={iconSize}
              />
            </Grid.Col>
          ))}
        </Grid>
      </Container>
    </Container>
  );
};
