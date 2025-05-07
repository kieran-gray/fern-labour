'use client';

import { ReactNode } from 'react';
import NextLink from 'next/link';
import {
  IconAdjustments,
  IconBellRinging,
  IconDeviceMobileMessage,
  IconMessage,
  IconMoodSmileBeam,
  IconSignLeft,
  IconUser,
  IconUsers,
} from '@tabler/icons-react';
import {
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

type Pricing01Props = {
  /** URL for the call to action button */
  callToActionUrl?: string;
};

export const Pricing01 = ({ callToActionUrl = '#' }: Pricing01Props) => {
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
            Free for Mums. Flexible for Family.
          </JumboTitle>
          <Text c="var(--mantine-color-gray-7)" ta="center" fz="xl" style={{ textWrap: 'balance' }}>
            Track labour for free. Let your loved ones stay in the loop, if they want to.
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
          title="For Mum"
          description=""
          cta={
            <Button
              component={NextLink}
              href={callToActionUrl}
              size="lg"
              radius="xl"
              variant="light"
              fullWidth
            >
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
              title: 'Peace of mind',
              description: 'No more constant messages or check-ins',
              icon: (
                <Icon>
                  <IconMoodSmileBeam size={21} />
                </Icon>
              ),
            },
            {
              title: 'You’re in control',
              description: 'Share updates only when you’re ready',
              icon: (
                <Icon>
                  <IconAdjustments size={21} />
                </Icon>
              ),
            },
          ]}
        />
        <PricingCard
          shadow="lg"
          title="For loved ones"
          description=""
          cta={
            <Button
              component={NextLink}
              radius="xl"
              href={callToActionUrl}
              variant="light"
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
          price="Free"
          pricingPeriod=""
          items={[
            {
              title: 'Subscribe',
              description: 'Subscribe to a labour',
              icon: (
                <Icon>
                  <IconUsers size={21} />
                </Icon>
              ),
            },
            {
              title: 'See updates in app',
              description: 'View labour updates in app',
              icon: (
                <Icon>
                  <IconMessage size={21} />
                </Icon>
              ),
            },
          ]}
        />
        <PricingCard
          title="For loved ones"
          description=""
          cta={
            <Button
              component={NextLink}
              href={callToActionUrl}
              radius="xl"
              size="lg"
              variant="light"
              fullWidth
            >
              Get started
            </Button>
          }
          icon={
            <Icon>
              <IconDeviceMobileMessage size={21} />
            </Icon>
          }
          price="£2.50"
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
              title: 'Live notifications',
              description: 'Real-time updates via WhatsApp/SMS',
              icon: (
                <Icon>
                  <IconBellRinging size={21} />
                </Icon>
              ),
            },
          ]}
        />
      </Group>
    </Container>
  );
};
