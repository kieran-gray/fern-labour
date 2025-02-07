import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Button, PinInput, Space, Title } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { ApiError, OpenAPI, SubscriberService, SubscribeToRequest } from '../../../client';
import baseClasses from '../../../shared-components/shared-styles.module.css';

export default function SubscribeForm({
  birthingPersonId,
  token,
}: {
  birthingPersonId: string;
  token: string | null;
}) {
  const auth = useAuth();
  const navigate = useNavigate();
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      token: token || '',
    },
    validate: {
      token: (value) => (value.length !== 8 ? 'Invalid token' : null),
    },
  });

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (values: typeof form.values) => {
      const requestBody: SubscribeToRequest = { token: values.token };
      const response =
        await SubscriberService.subscribeToApiV1SubscriberSubscribeToBirthingPersonIdPost({
          requestBody,
          birthingPersonId,
        });
      return response.subscriber;
    },
    onSuccess: (subscriber) => {
      queryClient.setQueryData(['subscriber', auth.user?.profile.sub], subscriber);
      navigate('/');
    },
    onError: (error) => {
      let message = 'Unknown error occurred';
      if (error instanceof ApiError) {
        try {
          const body = error.body as { description: string };
          message = body.description;
        } catch {
          // Do nothing
        }
      }
      notifications.show({
        title: 'Error',
        message,
        radius: 'lg',
        color: 'var(--mantine-color-pink-9)',
        classNames: {
          title: baseClasses.notificationTitle,
          description: baseClasses.notificationDescription,
        },
        style: {
          backgroundColor: 'var(--mantine-color-pink-4)',
          color: 'var(--mantine-color-white)',
        },
      });
    },
  });
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.header}>
        <div className={baseClasses.title}>Subscribe</div>
      </div>
      <div className={baseClasses.body}>
        <Title className={baseClasses.text}>Enter token to subscribe:</Title>
        <Space h="xl" />
        <form onSubmit={form.onSubmit((values) => mutation.mutate(values))}>
          <PinInput
            fw={600}
            size="lg"
            length={8}
            radius="md"
            key={form.key('token')}
            {...form.getInputProps('token')}
          />
          <Space h="xl" />
          <div className={baseClasses.flexRowEnd}>
            <Button
              color="var(--mantine-color-pink-4)"
              size="lg"
              radius="lg"
              variant="filled"
              type="submit"
            >
              Submit
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
