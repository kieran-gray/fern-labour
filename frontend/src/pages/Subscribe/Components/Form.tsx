import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Button, PinInput, Space, Title, Text, Image, Group } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { ApiError, OpenAPI, SubscriberService, SubscribeToRequest } from '../../../client';
import baseClasses from '../../../shared-components/shared-styles.module.css';
import classes from './Form.module.css';
import image from './image.svg';

const SUBSCRIBER_TOKEN_LENGTH = 5;

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
      token: (value) => (value.length !== SUBSCRIBER_TOKEN_LENGTH ? 'Invalid token' : null),
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
    <div className={baseClasses.root} style={{maxWidth: '1100px'}}>
      <div className={baseClasses.header}>
        <div className={baseClasses.title}>Subscribe</div>
      </div>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title className={classes.title}>
              Congratulations! <br/> Someone wants to share their labour journey with you!
            </Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              If the code isn't already filled in, check the share message that was sent to you, or ask the person who shared the link with you for the code.
            </Text>
            <Group mt={30}>
              <form onSubmit={form.onSubmit((values) => mutation.mutate(values))}>
                <div className={classes.flexRowEnd} style={{ alignItems: 'end' }}>
                  <PinInput
                    fw={600}
                    size="lg"
                    length={SUBSCRIBER_TOKEN_LENGTH}
                    radius="md"
                    key={form.key('token')}
                    {...form.getInputProps('token')}
                  />
                  <Space w="xl" h="xl" />
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
