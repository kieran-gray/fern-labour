import { useLabour } from '@base/contexts/LabourContext';
import { useApiAuth, useSendLabourInvite } from '@shared/hooks';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { validateEmail } from '@shared/utils';
import { IconAt, IconSend } from '@tabler/icons-react';
import { Button, Group, Image, Space, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import image from './invite.svg';
import classes from './InviteContainer.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export function InviteContainer() {
  useApiAuth();
  const { labourId } = useLabour();
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      email: '',
    },

    validate: {
      email: (value) => (validateEmail(value) ? null : 'Invalid email'),
    },
  });

  const sendInviteMutation = useSendLabourInvite();

  const handleSubmit = (values: typeof form.values) => {
    sendInviteMutation.mutate(
      {
        email: values.email,
        labourId: labourId!,
      },
      {
        onSuccess: () => {
          form.reset();
        },
      }
    );
  };

  const title = 'Or send invites by email';
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
          <form onSubmit={form.onSubmit(handleSubmit)} style={{ width: '100%' }}>
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
                loading={sendInviteMutation.isPending}
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
                loading={sendInviteMutation.isPending}
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
