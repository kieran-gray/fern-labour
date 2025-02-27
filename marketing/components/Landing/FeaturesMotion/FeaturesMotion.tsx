'use client';

import { ReactNode } from 'react';
import {
  IconAmbulance,
  IconBellRinging,
  IconCalendar,
  IconChartHistogram,
  IconMessage,
  IconSend,
  IconSpeakerphone,
  IconStopwatch,
  IconUsers,
} from '@tabler/icons-react';
import { motion } from 'motion/react';
import { Box, Card, Container, Flex, Grid, Stack, Text } from '@mantine/core';
import { JumboTitle } from '../JumboTitle/JumboTitle';
import classes from './FeaturesMotion.module.css';

type Feature = {
  icon: ReactNode;
  title: string;
  description: ReactNode;
};

const FEATURES: Feature[] = [
  {
    icon: <IconCalendar color="var(--mantine-color-pink-6)" />,
    title: 'Plan Your Labour',
    description: 'Share some basic details about your labour for a more customized experience.',
  },
  {
    icon: <IconStopwatch color="var(--mantine-color-pink-6)" />,
    title: 'Track Your Contractions',
    description: 'You can choose to track your contractions continuously, or in bursts.',
  },
  {
    icon: <IconAmbulance color="var(--mantine-color-pink-6)" />,
    title: 'Get To The Hospital On Time',
    description: 'We will alert you when it is time to go to the hospital.',
  },
  {
    icon: <IconChartHistogram color="var(--mantine-color-pink-6)" />,
    title: 'Detailed Statistics',
    description: 'Access detailed statistics about your contractions and labour progress.',
  },
  {
    icon: <IconSend color="var(--mantine-color-pink-6)" />,
    title: 'Invite Friends and Family',
    description: 'Share invites with your loved ones by email, link, or QR code.',
  },
  {
    icon: <IconMessage color="var(--mantine-color-pink-6)" />,
    title: 'Share Status Updates',
    description:
      'Keep loved ones up-to-date with status updates to prevent those annoying "Is the baby here yet?" messages.',
  },
  {
    icon: <IconBellRinging color="var(--mantine-color-pink-6)" />,
    title: 'Automatic Notifications',
    description:
      'Loved ones receive automatic text or email notifications when your labour begins.',
  },
  {
    icon: <IconSpeakerphone color="var(--mantine-color-pink-6)" />,
    title: 'Share Announcements',
    description: 'Send important updates to your loved ones by text or email during your labour.',
  },
  {
    icon: <IconUsers color="var(--mantine-color-pink-6)" />,
    title: 'Manage Your Subscribers',
    description:
      'Only people you invite can see your labour, and you can remove or block any unwanted subscribers.',
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
    transition={{ duration: 0.8, delay: 0.2 * index, ease: 'easeInOut' }}
    viewport={{ once: true }}
    style={{ height: '100%' }}
  >
    <motion.div
      whileHover={{ scale: 1.05, boxShadow: 'var(--mantine-shadow-xl)' }}
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
  features?: Feature[];
  iconSize?: number;
};

export const Feature02 = ({
  title = 'Features',
  features = FEATURES,
  iconSize = 20,
}: Feature02Props) => (
  <Container
    bg="var(--mantine-color-body)"
    py={{
      base: 'calc(var(--mantine-spacing-lg) * 4)',
      xs: 'calc(var(--mantine-spacing-lg) * 5)',
      lg: 'calc(var(--mantine-spacing-lg) * 6)',
    }}
    fluid
  >
    <Container size="lg" px={0} style={{ position: 'relative' }} id="#features">
      <JumboTitle order={2} fz="md" style={{ textWrap: 'balance' }}>
        {title}
      </JumboTitle>
    </Container>
    <Container size="lg" p={0} mt="xl">
      <Grid gutter="xl">
        {features.map((feature, index) => (
          <Grid.Col key={feature.title} span={{ base: 12, xs: 6, md: 4 }} mih="100%">
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
