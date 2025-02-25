import { useState } from 'react';
import { IconInfoCircle } from '@tabler/icons-react';
import { useMutation } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import Turnstile from 'react-turnstile';
import {
  Alert,
  Button,
  Group,
  SimpleGrid,
  Space,
  Text,
  Textarea,
  TextInput,
  Title,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { ContactUsService } from '../../../client/sdk.gen.ts';
import { ContactUsRequest } from '../../../client/types.gen.ts';
import { ContainerHeader } from '../../../shared-components/ContainerHeader/ContainerHeader.tsx';
import { ContactIconsList } from './ContactIcons.tsx';
import baseClasses from '../../../shared-components/shared-styles.module.css';
import classes from './ContactUs.module.css';

export function ContactUs() {
  const [status, setStatus] = useState({ type: '', message: '' });
  const [isLoading, setIsLoading] = useState(false);
  const [turnstileToken, setTurnstileToken] = useState<string | null>(null);
  const auth = useAuth();
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      email: auth.user?.profile.email || '',
      name: `${auth.user?.profile.given_name} ${auth.user?.profile.family_name}`,
      message: '',
    },
    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
    },
  });

  const mutation = useMutation({
    mutationFn: async (values: typeof form.values) => {
      setIsLoading(true);
      setStatus({ type: '', message: '' });
      const requestBody: ContactUsRequest = {
        email: values.email,
        name: values.name,
        message: values.message,
        token: turnstileToken!,
        user_id: auth.user?.profile.sub,
      };
      await ContactUsService.sendMessageApiV1ContactUsPost({ requestBody });
    },
    onSuccess: () => {
      form.setInitialValues({ email: '', name: '', message: '' });
      form.reset();
      setStatus({
        type: 'success',
        message: "Message sent successfully! We'll get back to you soon.",
      });
    },
    onError: (_) => {
      setStatus({
        type: 'error',
        message: 'Failed to send message. Please try again later.',
      });
    },
    onSettled: () => {
      setIsLoading(false);
    },
  });

  const alertIcon = <IconInfoCircle />;

  return (
    <div className={baseClasses.root}>
      <ContainerHeader title="Contact Us" />
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <SimpleGrid cols={{ base: 1, sm: 2 }} spacing={50}>
            <div>
              <Title order={3}>Send us a message</Title>
              <Text mt="sm" mb={30}>
                Leave your email and we will get back to you within 24 hours
              </Text>
              <ContactIconsList />
            </div>
            <form
              className={classes.form}
              onSubmit={form.onSubmit((values) => mutation.mutate(values))}
            >
              {status.type && (
                <Alert
                  variant="light"
                  color={status.type === 'success' ? 'green' : 'red'}
                  radius="md"
                  title={status.type}
                  icon={alertIcon}
                  mb={10}
                  withCloseButton
                  onClose={() => setStatus({ type: '', message: '' })}
                >
                  {status.message}
                </Alert>
              )}
              <TextInput
                required
                label="Email"
                key={form.key('email')}
                placeholder="your@email.com"
                classNames={{ input: classes.input, label: classes.inputLabel }}
                {...form.getInputProps('email')}
              />
              <TextInput
                required
                label="Name"
                key={form.key('name')}
                placeholder="John Doe"
                mt="md"
                classNames={{ input: classes.input, label: classes.inputLabel }}
                {...form.getInputProps('name')}
              />
              <Textarea
                required
                label="Your message"
                key={form.key('message')}
                placeholder="Your message..."
                minRows={4}
                mt="md"
                classNames={{ input: classes.input, label: classes.inputLabel }}
                {...form.getInputProps('message')}
              />
              <Space h={10} />
              <Turnstile
                sitekey="0x4AAAAAAA-eKMn9GfnERlf2"
                onVerify={(token) => setTurnstileToken(token)}
              />
              <Group justify="flex-end" mt="md">
                <Button
                  type="submit"
                  className={classes.control}
                  radius="lg"
                  loading={isLoading}
                  disabled={status.type === 'success' || turnstileToken === null}
                >
                  {isLoading ? 'Sending...' : 'Send Message'}
                </Button>
              </Group>
            </form>
          </SimpleGrid>
        </div>
      </div>
    </div>
  );
}
