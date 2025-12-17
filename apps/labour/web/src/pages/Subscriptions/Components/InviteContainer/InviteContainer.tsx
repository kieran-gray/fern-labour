import { validateEmail } from '@base/shared-components/utils';
import image from '@labour/Tabs/Invites/InviteContainer/invite.svg';
import { useApiAuth } from '@shared/hooks';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { IconAt, IconSend } from '@tabler/icons-react';
import { Button, Group, Image, Space, TextInput } from '@mantine/core';
import { useForm } from '@mantine/form';
import classes from '@labour/Tabs/Invites/InviteContainer/InviteContainer.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export function InviteContainer() {
  useApiAuth();
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      email: '',
    },

    validate: {
      email: (value) => (validateEmail(value) ? null : 'Invalid email'),
    },
  });

  const handleSubmit = (_values: typeof form.values) => {
    // sendInviteMutation.mutate(values.email, {
    //   onSuccess: () => {
    //     form.reset();
    //   },
    // });
  };

  const title = 'Know an expecting mum? Invite her to join!';
  const description =
    'Introduce her to a simple way to keep family and friends informed throughout her labour experience.';

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <Image src={image} className={classes.image} />
          <div className={baseClasses.content}>
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
                    placeholder="mum@email.com"
                    key={form.key('email')}
                    size="lg"
                    {...form.getInputProps('email')}
                    classNames={{
                      description: baseClasses.description,
                      input: baseClasses.input,
                      section: baseClasses.section,
                    }}
                  />
                  <Space w="md" />
                  <Button
                    color="var(--mantine-primary-color-4)"
                    variant="filled"
                    rightSection={<IconSend size={20} stroke={1.5} />}
                    radius="xl"
                    size="md"
                    pr={14}
                    h={48}
                    mt="var(--mantine-spacing-lg)"
                    styles={{ section: { marginLeft: 22 }, label: { overflow: 'unset' } }}
                    type="submit"
                    loading={false}
                  >
                    Send invite
                  </Button>
                </div>
              </form>
            </Group>
          </div>
        </div>
      </div>
    </div>
  );
}
