import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Button, Group, Image, PinInput, Space, Text, Title } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { OpenAPI, SubscribeToRequest, SubscriptionService } from '../../../clients/labour_service';
import { AppMode, useMode } from '../../Home/SelectAppMode';
import image from './protected.svg';
import baseClasses from '../../../shared-components/shared-styles.module.css';
import classes from './Form.module.css';

const SUBSCRIBER_TOKEN_LENGTH = 5;

export default function SubscribeForm({
  labourId,
  token,
}: {
  labourId: string;
  token: string | null;
}) {
  const [mutationInProgress, setMutationInProgress] = useState(false);
  const auth = useAuth();
  const navigate = useNavigate();
  const { setMode } = useMode();
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      token: token || '',
    },
    validate: {
      token: (value) => (value.length !== SUBSCRIBER_TOKEN_LENGTH ? 'Invalid token' : null),
    },
  });

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (values: typeof form.values) => {
      setMutationInProgress(true);
      const requestBody: SubscribeToRequest = { token: values.token };
      const response = await SubscriptionService.subscribeTo({ requestBody, labourId });
      return response.subscription;
    },
    onSuccess: (subscription) => {
      queryClient.setQueryData(
        ['subscription', subscription.id, auth.user?.profile.sub],
        subscription
      );
      setMode(AppMode.Subscriber);
      navigate(`/?prompt=requested`);
    },
    onError: () => {
      notifications.show({
        title: 'Error',
        message: 'Token or Labour ID is incorrect.',
        radius: 'lg',
        color: 'var(--mantine-color-primary-7)',
      });
    },
    onSettled: () => {
      setMutationInProgress(false);
    },
  });

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <div className={classes.content}>
            <Title className={classes.title}>
              Congratulations! <br /> Someone wants to share their labour journey with you!
            </Title>
            <div className={baseClasses.imageFlexRow}>
              <Image src={image} className={baseClasses.smallImage} />
            </div>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              If the code isn't already filled in, check the share message that was sent to you, or
              ask the person who shared the link with you for the code.
            </Text>
            <Group mt={30}>
              <form
                onSubmit={form.onSubmit((values) => mutation.mutate(values))}
                className={classes.form}
              >
                <div className={baseClasses.flexRowEnd}>
                  <PinInput
                    fw={600}
                    size="lg"
                    length={SUBSCRIBER_TOKEN_LENGTH}
                    radius="md"
                    style={{ justifyContent: 'center' }}
                    key={form.key('token')}
                    {...form.getInputProps('token')}
                  />
                  <Space w="xl" h="xl" />
                  <Button
                    color="var(--mantine-color-primary-4)"
                    size="lg"
                    radius="lg"
                    variant="filled"
                    type="submit"
                    loading={mutationInProgress}
                  >
                    Submit
                  </Button>
                </div>
              </form>
            </Group>
          </div>
          <Image src={image} className={classes.image} />
        </div>
      </div>
    </div>
  );
}
