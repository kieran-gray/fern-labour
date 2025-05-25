import { useState } from 'react';
import { ApiError, LabourService, OpenAPI, SendInviteRequest } from '@clients/labour_service';
import { useLabour } from '@labour/LabourContext';
import { Error, Success } from '@shared/Notifications';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { IconAt, IconSend } from '@tabler/icons-react';
import { useMutation } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button, Group, Image, Space, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import image from './invite.svg';
import classes from './InviteContainer.module.css';
import baseClasses from '@shared/shared-styles.module.css';

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
      await LabourService.sendInvite({ requestBody });
    },
    onSuccess: () => {
      notifications.show({
        ...Success,
        title: 'Success',
        message: `Invite email sent`,
      });
      form.reset();
    },
    onError: (err) => {
      if (err instanceof ApiError && err.status === 429) {
        notifications.show({
          ...Error,
          title: 'Slow down!',
          message: 'You have sent too many invites today. Wait until tomorrow to send more.',
        });
      } else {
        notifications.show({
          ...Error,
          title: 'Error sending invite',
          message: 'Something went wrong. Please try again.',
        });
      }
    },
    onSettled: () => {
      setMutationInProgress(false);
    },
  });

  const title = 'Invite friends and family by email';
  const description =
    "Invite your friends and family, we'll give them instructions on how to sign up and what to expect.";

  return (
    <div className={baseClasses.inner}>
      <Image src={image} className={classes.image} />
      <div className={classes.content}>
        <ResponsiveTitle title={title} />
        <ResponsiveDescription description={description} marginTop={10} />
        <div className={classes.imageFlexRow}>
          <Image src={image} className={classes.smallImage} />
        </div>
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
                classNames={{
                  description: baseClasses.description,
                  input: baseClasses.input,
                  section: baseClasses.section,
                }}
                {...form.getInputProps('email')}
              />
              <Space w="md" />
              <Button
                color="var(--mantine-primary-color-4)"
                variant="filled"
                rightSection={<IconSend size={20} stroke={1.5} />}
                radius="xl"
                size="lg"
                pr={14}
                mt="var(--mantine-spacing-lg)"
                loading={mutationInProgress}
                styles={{ section: { marginLeft: 22 }, label: { overflow: 'unset' } }}
                type="submit"
                visibleFrom="sm"
              >
                Send invite
              </Button>
              <Button
                color="var(--mantine-primary-color-4)"
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
                hiddenFrom="sm"
              >
                Send invite
              </Button>
            </div>
          </form>
        </Group>
      </div>
    </div>
  );
}
