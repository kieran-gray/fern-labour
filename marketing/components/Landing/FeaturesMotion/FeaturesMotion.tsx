'use client';

import { ReactNode, useMemo, useState } from 'react';
import {
  IconCurrencyPound,
  IconLock,
  IconMail,
  IconMessage,
  IconStopwatch,
  IconUsers,
} from '@tabler/icons-react';
import { motion } from 'motion/react';
import { Box, Card, Container, Flex, Grid, SegmentedControl, Stack, Text } from '@mantine/core';
import { JumboTitle } from '../JumboTitle/JumboTitle';
import classes from './FeaturesMotion.module.css';

type Feature = {
  icon: ReactNode;
  title: string;
  description: ReactNode;
};

const MUM_FEATURES: Feature[] = [
  {
    icon: <IconUsers color="var(--mantine-color-pink-6)" />,
    title: 'Create Your Circle',
    description: 'Send secure invites to family members who matter most to you.',
  },
  {
    icon: <IconStopwatch color="var(--mantine-color-pink-6)" />,
    title: 'Track Contractions',
    description: 'Simple one-tap tracking with automatic timing and intensity logging.',
  },
  {
    icon: <IconMessage color="var(--mantine-color-pink-6)" />,
    title: 'Share Updates',
    description:
      'Keep your loved ones informed before and during your labour with one-tap status updates.',
  },
  {
    icon: <IconLock color="var(--mantine-color-pink-6)" />,
    title: 'Full Control',
    description: 'Add or remove people anytime. Your labour, your guest list.',
  },
] as const;

const SUBSCRIBER_FEATURES: Feature[] = [
  {
    icon: <IconMail color="var(--mantine-color-pink-6)" />,
    title: 'Receive Invitation',
    description: 'Get a secure invite via email, text, or QR code from your loved one.',
  },
  {
    icon: <IconUsers color="var(--mantine-color-pink-6)" />,
    title: 'Join Their Circle',
    description: 'Quick signup and approval process to connect to their labour journey.',
  },
  {
    icon: <IconMessage color="var(--mantine-color-pink-6)" />,
    title: 'Real-time Updates',
    description: 'Stay informed with automatic notifications as labour progresses.',
  },
  {
    icon: <IconCurrencyPound color="var(--mantine-color-pink-6)" />,
    title: 'Premium Features',
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
              {title}
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
    <Container py={80} px="15px" fluid>
      <Container size="lg" px={0} style={{ position: 'relative' }} id="#features">
        <JumboTitle order={2} fz="xs" ta="center" style={{ textWrap: 'balance' }} mb={60}>
          {title}
        </JumboTitle>
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
            <Grid.Col key={`${feature.title}-${mode}`} span={{ base: 12, sm: 6 }} mih="100%">
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
