import { useState } from 'react';
import { IconInfoCircle } from '@tabler/icons-react';
import Turnstile from 'react-turnstile';
import {
  Alert,
  Button,
  Container,
  Group,
  SimpleGrid,
  Space,
  Text,
  Textarea,
  TextInput,
  Title,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { ContactIconsList } from './ContactIcons.tsx';
import classes from './ContactUs.module.css';

export function ContactUs() {
  const [status, setStatus] = useState({ type: '', message: '' });
  const [isLoading, setIsLoading] = useState(false);
  const [turnstileToken, setTurnstileToken] = useState<string | null>(null);
  const icon = <IconInfoCircle />;
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      email: '',
      name: '',
      message: '',
    },

    validate: {
      email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
    },
  });

  const contactServiceURL = process.env.NEXT_PUBLIC_CONTACT_SERVICE_URL;

  const handleSubmit = async (values: typeof form.values) => {
    setIsLoading(true);
    setStatus({ type: '', message: '' });

    try {
      const response = await fetch(`${contactServiceURL}/api/v1/contact-us/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: values.email,
          name: values.name,
          message: values.message,
          token: turnstileToken,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      form.reset();
      setStatus({
        type: 'success',
        message: "Message sent successfully! We'll get back to you soon.",
      });
    } catch (error) {
      setStatus({
        type: 'error',
        message: 'Failed to send message. Please try again later.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container mt={20} className={classes.wrapper} size="lg">
      <SimpleGrid cols={{ base: 1, sm: 2 }} spacing={50}>
        <div>
          <Title className={classes.title}>Contact us</Title>
          <Text className={classes.description} mt="sm" mb={30}>
            Leave your email and we will get back to you within 24 hours
          </Text>
          <ContactIconsList />
        </div>
        <form className={classes.form} onSubmit={form.onSubmit((values) => handleSubmit(values))}>
          {status.type && (
            <Alert
              variant="light"
              color={status.type === 'success' ? 'green' : 'red'}
              radius="md"
              title={status.type}
              icon={icon}
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
              disabled={isLoading || status.type === 'success'}
            >
              {isLoading ? 'Sending...' : 'Send Message'}
            </Button>
          </Group>
        </form>
      </SimpleGrid>
    </Container>
  );
}
