import { IconAt } from '@tabler/icons-react';
import { useMutation } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Text, TextInput, Title, Image, Group, Space } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { BirthingPersonService, OpenAPI, SendInviteRequest } from '../../../../client';
import { SendInviteButton } from '../SendInviteButton/SendInviteButton';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import image from './invite.svg';
import classes from './InviteContainer.module.css'

export function InviteContainer() {
  const auth = useAuth();
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      email: '',
    },

    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
    },
  });

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const mutation = useMutation({
    mutationFn: async (values: typeof form.values) => {
      const requestBody: SendInviteRequest = { invite_email: values.email };
      await BirthingPersonService.sendInviteApiV1BirthingPersonSendInvitePost({
        requestBody,
      });
    },
    onSuccess: () => {
      notifications.show({
        title: 'Success',
        message: `Invite email sent`,
        radius: 'lg',
        color: 'var(--mantine-color-green-3)',
        classNames: {
          title: baseClasses.notificationSuccessTitle,
          description: baseClasses.notificationSuccessDescription,
        },
        style: { backgroundColor: 'var(--mantine-color-pink-1)' },
      });
      form.reset();
    },
    onError: (error) => {
      console.error('Error sending invite', error);
    },
  });

  return (
    <div className={baseClasses.root} style={{maxWidth: '1100px'}}>
      <div className={baseClasses.header}>
        <Title fz="xl" className={baseClasses.title}>
          Invite
        </Title>
      </div>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title className={classes.title}>
              Invite friends and family by email
            </Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              Invite your friends and family to keep them in the loop and let them track your labour in real time.
              They’ll be able to support you every step of the way!
            </Text>
            <Group mt={30}>
              <form onSubmit={form.onSubmit((values) => mutation.mutate(values))}>
                <div className={classes.flexRowEnd} style={{ alignItems: 'end' }}>
                  <TextInput
                    withAsterisk
                    radius="lg"
                    mt="md"
                    rightSectionPointerEvents="none"
                    rightSection={<IconAt size={16} />}
                    label="Email"
                    placeholder="friend@email.com"
                    key={form.key('email')}
                    size="md"
                    {...form.getInputProps('email')}
                  />
                  <Space w="md" />
                  <SendInviteButton />
                </div>
              </form>
            </Group>
          </div>
          <Image src={image} className={classes.image} />
        </div>
      </div>
    </div>
  )
}
