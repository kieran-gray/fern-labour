import { useState } from 'react';
import { IconBrandInstagram, IconInfoCircle } from '@tabler/icons-react';
import {
  ActionIcon,
  Alert,
  Button,
  Container,
  Group,
  SimpleGrid,
  Text,
  Textarea,
  TextInput,
  Title,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { ContactIconsList } from './ContactIcons.tsx';
import classes from './ContactUs.module.css';

const social = [{ icon: IconBrandInstagram, link: process.env.NEXT_PUBLIC_INSTAGRAM_URL, title: 'Instagram' }];

export function ContactUs() {
  const [status, setStatus] = useState({ type: '', message: '' });
  const [isLoading, setIsLoading] = useState(false);
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

  const backendApiUrl = process.env.NEXT_PUBLIC_BACKEND_API_URL;

  const handleSubmit = async (values: typeof form.values) => {
    setIsLoading(true);
    setStatus({ type: '', message: '' });

    try {
      const response = await fetch(`${backendApiUrl}/api/v1/contact-us/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values),
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

  const icons = social.map((data, index) => (
    <ActionIcon
      target="_blank"
      key={index}
      component="a"
      href={data.link}
      size={28}
      className={classes.social}
      variant="transparent"
      title={data.title}

    >
      <data.icon size={22} stroke={1.5} />
    </ActionIcon>
  ));

  return (
    <Container mt={20} className={classes.wrapper} size="lg">
      <SimpleGrid cols={{ base: 1, sm: 2 }} spacing={50}>
        <div>
          <Title className={classes.title}>Contact us</Title>
          <Text className={classes.description} mt="sm" mb={30}>
            Leave your email and we will get back to you within 24 hours
          </Text>
          <ContactIconsList />
          <Group mt="xl">{icons}</Group>
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
