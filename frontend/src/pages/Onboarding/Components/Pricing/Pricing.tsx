'use client';

import { ReactNode, useState } from 'react';
import {
  IconAmbulance,
  IconChartHistogram,
  IconDots,
  IconMessage,
  IconSignLeft,
  IconSpeakerphone,
  IconStopwatch,
  IconUser,
  IconUsers,
  IconUsersGroup,
} from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Carousel } from '@mantine/carousel';
import {
  Badge,
  Box,
  Button,
  Card,
  CardProps,
  Center,
  Divider,
  Flex,
  Group,
  Image,
  LoadingOverlay,
  Space,
  Stack,
  Text,
  Title,
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
  CreateCheckoutRequest,
  LabourDTO,
  LabourService,
  OpenAPI,
  PaymentPlanLabourRequest,
  PaymentsService,
} from '../../../../client';
import { useLabour } from '../../../Labour/LabourContext';
import image from './thanks.svg';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
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
    miw={270}
    maw={380}
    withBorder
    className={classes.root}
    style={{ flexGrow: 1 }}
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
      <Title my={0} mb="sm" c="var(--mantine-color-pink-4)">
        {price}
      </Title>
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
            <Text fw={500} visibleFrom="sm">
              {item.title}
            </Text>
            <Text c="dimmed" fz="sm" inline visibleFrom="sm">
              {item.description}
            </Text>
            <Text fw={500} fz="sm" hiddenFrom="sm">
              {item.title}
            </Text>
            <Text c="dimmed" fz="xs" inline hiddenFrom="sm">
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

export const Pricing01 = ({ labour }: { labour: LabourDTO | undefined }) => {
  const auth = useAuth();
  const navigate = useNavigate();
  const { labourId } = useLabour();
  const [searchParams] = useSearchParams();
  const cancelled = searchParams.get('cancelled');
  const success = searchParams.get('success');
  const [mutationInProgress, setMutationInProgress] = useState<boolean>(false);

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const setInitialStep = (): number => {
    let initialSlide = 0;
    if (labour?.payment_plan === null) {
      initialSlide = 1;
    }
    if (cancelled) {
      initialSlide = 0;
    }
    return initialSlide;
  };

  const mutation = useMutation({
    mutationFn: async ({ selectedPlan }: { selectedPlan: string }) => {
      setMutationInProgress(true);
      const requestBody: PaymentPlanLabourRequest = { payment_plan: selectedPlan };
      const response = await LabourService.updateLabourPaymentPlanApiV1LabourPaymentPlanPut({
        requestBody,
      });
      return response.labour;
    },
    onSuccess: async (labour) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
      setMutationInProgress(false);
      navigate('/');
    },
    onError: async () => {
      setMutationInProgress(false);
      notifications.show({
        title: 'Error Updating Labour Payment Plan',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
    },
    onSettled: () => {
      setMutationInProgress(false);
    },
  });

  const stripeCheckout = useMutation({
    mutationFn: async () => {
      setMutationInProgress(true);
      const currentUrl = window.location.href;

      const successUrl = new URL(currentUrl);
      successUrl.searchParams.set('success', 'true');

      const cancelUrl = new URL(currentUrl);
      cancelUrl.searchParams.set('cancelled', 'true');

      const requestBody: CreateCheckoutRequest = {
        upgrade: 'inner_circle',
        labour_id: labourId!,
        success_url: successUrl.toString(),
        cancel_url: cancelUrl.toString(),
      };
      return await PaymentsService.createCheckoutSessionApiV1PaymentsCreateCheckoutSessionPost({
        requestBody,
      });
    },
    onSuccess: async (data) => {
      window.location.href = data.url;
      queryClient.invalidateQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      setMutationInProgress(false);
    },
    onError: async () => {
      setMutationInProgress(false);
      notifications.show({
        title: 'Error',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
    },
    onSettled: () => {
      setMutationInProgress(false);
    },
  });

  const soloCard = (
    <PricingCard
      title="Solo"
      description=""
      cta={
        <Button
          size="lg"
          radius="xl"
          variant="light"
          fullWidth
          onClick={() => mutation.mutate({ selectedPlan: 'solo' })}
          loading={mutationInProgress}
        >
          Start for Free
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
  );

  const innerCircleCard = (
    <PricingCard
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
          radius="xl"
          size="lg"
          bg="var(--mantine-color-pink-5)"
          fullWidth
          variant={labour?.payment_plan === 'inner_circle' ? 'light' : 'filled'}
          disabled={labour?.payment_plan === 'inner_circle'}
          onClick={() => stripeCheckout.mutate()}
        >
          {labour?.payment_plan === 'inner_circle' ? 'Your current plan' : 'Go To Payment'}
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
  );

  const communityCard = (
    <PricingCard
      badge={
        <Badge variant="outline" size="lg">
          Best Value
        </Badge>
      }
      title="Community"
      description=""
      cta={
        <Button
          radius="xl"
          size="lg"
          fullWidth
          variant={labour?.payment_plan === 'community' ? 'light' : 'filled'}
          onClick={() => stripeCheckout.mutate()}
          disabled={labour?.payment_plan === 'community'}
        >
          {labour?.payment_plan === 'community' ? 'Your current plan' : 'Go To Payment'}
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
          title: 'Coming soon',
          description: 'More features in progress',
          icon: (
            <Icon>
              <IconDots size={21} />
            </Icon>
          ),
        },
      ]}
    />
  );

  if (success) {
    return (
      <div className={baseClasses.flexColumn} style={{ width: '100%', position: 'relative' }}>
        <div className={baseClasses.inner} style={{ padding: 0 }}>
          <div className={baseClasses.content}>
            <Title order={2}>Your Journey Begins!</Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              Payment confirmed. Thank you for choosing fernlabour.com.
              <br />
              <br />
              Your birth story deserves to be shared with those who matter most. We're honoured to
              help you connect with your loved ones during this special time.
              <br />
              <br />
              Need help? Our support team is ready to assist at support@fernlabour.com.
            </Text>
            <div className={baseClasses.imageFlexRow}>
              <Image src={image} className={classes.smallImage} />
            </div>
          </div>
          <div className={baseClasses.flexColumn}>
            <Image src={image} className={classes.image} />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={baseClasses.flexColumn} style={{ width: '100%', position: 'relative' }}>
      <LoadingOverlay
        visible={mutationInProgress}
        zIndex={1001}
        overlayProps={{ radius: 'sm', blur: 3 }}
      />
      <Title order={2}>Choose Your Birth Support Plan</Title>
      <Text c="var(--mantine-color-gray-7)" mt="md">
        Select how you'd like to share your birth experience with family and friends.
        <br />
        Choose between our affordable Inner-Circle option or our comprehensive Community plan to
        keep loved ones updated throughout your journey. Or track your contractions for free with
        the Solo plan.
      </Text>
      <Space h="lg" />
      <Carousel
        height="100%"
        slideSize={{ base: '100%', '750px': '50%' }}
        slideGap={{ base: 0, '300px': 'md', '500px': 'lg' }}
        classNames={{ slide: classes.slide, control: classes.control }}
        type="container"
        align="start"
        style={{ flexGrow: 1 }}
        initialSlide={setInitialStep()}
      >
        {labour?.payment_plan === null && <Carousel.Slide>{soloCard}</Carousel.Slide>}
        {labour?.payment_plan !== 'community' && <Carousel.Slide>{innerCircleCard}</Carousel.Slide>}
        <Carousel.Slide>{communityCard}</Carousel.Slide>
      </Carousel>
    </div>
  );
};
