import { useState } from 'react';
import { IconAt, IconSend } from '@tabler/icons-react';
import { useMutation } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button, Group, Image, Space, Text, TextInput, Title } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { LabourService, OpenAPI, SendInviteRequest } from '../../../../../client';
import { ContainerHeader } from '../../../../../shared-components/ContainerHeader/ContainerHeader';
import { useLabour } from '../../../LabourContext';
import image from './invite.svg';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
import classes from './InviteContainer.module.css';

export function InviteContainer() {
  const auth = useAuth();
  const { labourId } = useLabour();
  const [mutationInProgress, setMutationInProgress] = useState(false);
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
      setMutationInProgress(true);
      const requestBody: SendInviteRequest = { invite_email: values.email, labour_id: labourId! };
      await LabourService.sendInviteApiV1LabourSendInvitePost({
        requestBody,
      });
    },
    onSuccess: () => {
      notifications.show({
        title: 'Success',
        message: `Invite email sent`,
        radius: 'lg',
        color: 'var(--mantine-color-green-3)',
      });
      form.reset();
    },
    onError: () => {
      notifications.show({
        title: 'Error sending invite',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
    },
    onSettled: () => {
      setMutationInProgress(false);
    },
  });

  return (
    <div className={baseClasses.root}>
      <ContainerHeader title="Invite" />
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title order={3}>Invite friends and family by email</Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              Invite your friends and family to keep them in the loop and let them track your labour
              in real time. They’ll be able to support you every step of the way!
            </Text>
            <Group className={classes.group}>
              <form
                onSubmit={form.onSubmit((values) => mutation.mutate(values))}
                style={{ width: '100%' }}
              >
                <div className={classes.flexRowEnd}>
                  <TextInput
                    withAsterisk
                    radius="lg"
                    mt="md"
                    rightSectionPointerEvents="none"
                    rightSection={<IconAt size={16} />}
                    label="Email"
                    placeholder="friend@email.com"
                    key={form.key('email')}
                    size="lg"
                    {...form.getInputProps('email')}
                  />
                  <Space w="md" />
                  <Button
                    color="var(--mantine-color-pink-4)"
                    variant="filled"
                    rightSection={<IconSend size={20} stroke={1.5} />}
                    radius="xl"
                    size="md"
                    pr={14}
                    h={48}
                    mt="var(--mantine-spacing-lg)"
                    loading={mutationInProgress}
                    styles={{ section: { marginLeft: 22 }, label: { overflow: 'unset' } }}
                    type="submit"
                  >
                    Send invite
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
