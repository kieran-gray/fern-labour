import NextLink from 'next/link';
import { IconArrowUpRight } from '@tabler/icons-react';
import { Button, Card, Container, Stack, Text } from '@mantine/core';
import { JumboTitle } from '../JumboTitle/JumboTitle';

export type CallToActionProps = {
  title: string;
  description: string;
  cta: string;
};

export const CallToAction01 = ({ title, description, cta }: CallToActionProps) => (
  <Container
    py={{
      base: 'calc(var(--mantine-spacing-lg))',
      xs: 'calc(var(--mantine-spacing-lg) * 2)',
      lg: 'calc(var(--mantine-spacing-lg) * 3)',
    }}
    px={0}
    w="100%"
  >
    <Container w="100%">
      <Card radius="lg" mih={400} bg="transparent">
        <Stack align="center" justify="center" h="100%" gap="xl" flex={1}>
          <JumboTitle
            order={2}
            fz="xs"
            ta="center"
            style={{ textWrap: 'balance' }}
            mb="sm"
            maw="80%"
          >
            {title}
          </JumboTitle>
          <Text
            ta="center"
            maw="var(--mantine-breakpoint-xs)"
            fz="xl"
            style={{ textWrap: 'balance' }}
          >
            {description}
          </Text>
          <Button
            component={NextLink}
            href="https://track.fernlabour.com"
            radius="xl"
            size="lg"
            rightSection={<IconArrowUpRight />}
          >
            {cta}
          </Button>
        </Stack>
      </Card>
    </Container>
  </Container>
);
