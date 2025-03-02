'use client';

import { ReactNode } from 'react';
import NextLink from 'next/link';
import {
  IconAmbulance,
  IconChartHistogram,
  IconDeviceMobile,
  IconMessage,
  IconSignLeft,
  IconSpeakerphone,
  IconStopwatch,
  IconUser,
  IconUsers,
  IconUsersGroup,
} from '@tabler/icons-react';
import {
  Badge,
  Box,
  Button,
  Card,
  CardProps,
  Center,
  Container,
  Divider,
  Flex,
  Group,
  Stack,
  Text,
} from '@mantine/core';
import { JumboTitle } from '../JumboTitle/JumboTitle';
import classes from './Pricing.module.css';

const Icon = ({ children }: { children: ReactNode }) => (
  <Card radius="xl" p="sm" withBorder>
    <Center>{children}</Center>
  </Card>
);

const PricingCard = ({
  badge,
  cta,
  description,
  icon,
  items,
  price,
  pricingPeriod,
  title,
  shadow,
  strikethroughPrice,
  showStrikethroughPrice = true,
}: {
  badge?: ReactNode;
  cta: ReactNode;
  description: string;
  icon: ReactNode;
  items: Array<{
    description: string;
    icon: ReactNode;
    title: string;
  }>;
  price: string;
  pricingPeriod: string;
  shadow?: CardProps['shadow'];
  strikethroughPrice?: string;
  showStrikethroughPrice?: boolean;
  title: string;
}) => (
  <Card
    radius="xl"
    shadow={shadow}
    miw={{ base: '100%', sm: 350 }}
    maw={380}
    withBorder
    className={classes.root}
  >
    <Group justify="space-between" align="start" mb="md">
      <Box>{icon}</Box>
      <Box>{badge}</Box>
    </Group>
    <Text fz="xl" fw="bold">
      {title}
    </Text>
    <Text mb="md" c="dimmed">
      {description}
    </Text>
    <Text
      c="dimmed"
      fz="lg"
      td="line-through"
      span
      style={{ visibility: showStrikethroughPrice ? 'visible' : 'hidden' }}
    >
      {strikethroughPrice}
    </Text>
    <Flex align="end" gap="xs">
      <JumboTitle my={0} order={2} fz="md" mb="sm" c="var(--mantine-color-pink-4)">
        {price}
      </JumboTitle>
      <Text c="dimmed" span>
        {pricingPeriod}
      </Text>
    </Flex>
    <Card.Section my="lg">
      <Divider />
    </Card.Section>
    <Stack>
      {items.map((item) => (
        <Group key={item.title} gap="xs">
          <Box>{item.icon}</Box>
          <Stack gap={0}>
            <Text fw={500}>{item.title}</Text>
            <Text c="dimmed" fz="sm" inline>
              {item.description}
            </Text>
          </Stack>
        </Group>
      ))}
    </Stack>
    <Card.Section my="lg">
      <Divider />
    </Card.Section>
    <Box>{cta}</Box>
  </Card>
);

export const Pricing01 = () => {
  return (
    <Container
      bg="var(--mantine-color-body)"
      py={{
        base: 'calc(var(--mantine-spacing-lg) * 1)',
        xs: 'calc(var(--mantine-spacing-lg) * 2)',
        lg: 'calc(var(--mantine-spacing-lg) * 3)',
      }}
      fluid
    >
      <Container size="md" id="#pricing" style={{ position: 'relative' }}>
        <Stack align="center" gap="xs">
          <JumboTitle order={2} fz="md" ta="center" style={{ textWrap: 'balance' }}>
            Simple, per-labour pricing
          </JumboTitle>
          <Text c="var(--mantine-color-gray-7)" ta="center" fz="xl" style={{ textWrap: 'balance' }}>
            No unnecessary subscriptions, just pay to upgrade your labour.
          </Text>
        </Stack>
      </Container>
      <Group
        mt={{
          base: 'calc(var(--mantine-spacing-lg) * 2)',
          lg: 'calc(var(--mantine-spacing-lg) * 3)',
        }}
        justify="center"
        gap="xl"
      >
        <PricingCard
          title="Solo"
          description=""
          cta={
            <Button component={NextLink} href="#" size="lg" radius="xl" variant="light" fullWidth>
              Get started
            </Button>
          }
          icon={
            <Icon>
              <IconUser size={21} />
            </Icon>
          }
          price="Free"
          pricingPeriod=""
          items={[
            {
              title: 'Track your contractions',
              description: 'Access to the contraction tracker',
              icon: (
                <Icon>
                  <IconStopwatch size={21} />
                </Icon>
              ),
            },
            {
              title: 'Get to the hospital on time',
              description: 'Contraction based alerts throughout',
              icon: (
                <Icon>
                  <IconAmbulance size={21} />
                </Icon>
              ),
            },
            {
              title: 'Statistics',
              description: 'See your contraction statistics',
              icon: (
                <Icon>
                  <IconChartHistogram size={21} />
                </Icon>
              ),
            },
          ]}
        />
        <PricingCard
          shadow="lg"
          badge={
            <Badge variant="light" size="lg">
              Most popular
            </Badge>
          }
          title="Inner-Circle"
          description=""
          cta={
            <Button
              className={classes.cta}
              component={NextLink}
              radius="xl"
              href="#"
              size="lg"
              fullWidth
            >
              Get started
            </Button>
          }
          icon={
            <Icon>
              <IconUsers size={21} />
            </Icon>
          }
          price="£10"
          pricingPeriod=""
          items={[
            {
              title: 'Status Updates',
              description: 'Share updates with loved ones',
              icon: (
                <Icon>
                  <IconMessage size={21} />
                </Icon>
              ),
            },
            {
              title: 'Up to 5 Subscribers',
              description: 'Slots for 5 loved ones to follow you',
              icon: (
                <Icon>
                  <IconUsers size={21} />
                </Icon>
              ),
            },
            {
              title: 'Make announcements',
              description: 'Send text messages to loved ones',
              icon: (
                <Icon>
                  <IconSpeakerphone size={21} />
                </Icon>
              ),
            },
          ]}
        />
        <PricingCard
          badge={
            <Badge variant="outline" size="lg">
              Best Value
            </Badge>
          }
          title="Community"
          description=""
          cta={
            <Button component={NextLink} href="#" radius="xl" size="lg" variant="light" fullWidth>
              Get started
            </Button>
          }
          icon={
            <Icon>
              <IconUsersGroup size={21} />
            </Icon>
          }
          price="£15"
          pricingPeriod=""
          items={[
            {
              title: 'All of the previous',
              description: 'Plus the following...',
              icon: (
                <Icon>
                  <IconSignLeft size={21} />
                </Icon>
              ),
            },
            {
              title: 'Unlimited Subscribers',
              description: 'Have unlimited friends and family join',
              icon: (
                <Icon>
                  <IconUsersGroup size={21} />
                </Icon>
              ),
            },
            {
              title: 'Allocate Birth Partner',
              description: 'So they can track for you from their device',
              icon: (
                <Icon>
                  <IconDeviceMobile size={21} />
                </Icon>
              ),
            },
          ]}
        />
      </Group>
    </Container>
  );
};
