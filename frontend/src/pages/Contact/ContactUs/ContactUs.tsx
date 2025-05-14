import { useState } from 'react';
import { IconInfoCircle } from '@tabler/icons-react';
import { useMutation } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import Turnstile from 'react-turnstile';
import {
  Alert,
  Button,
  Checkbox,
  Group,
  Rating,
  Select,
  SimpleGrid,
  Space,
  Text,
  Textarea,
  Title,
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { ContactUsService } from '../../../clients/contact_service/sdk.gen.ts';
import { ContactUsRequest } from '../../../clients/contact_service/types.gen.ts';
import { ContactIconsList } from './ContactIcons.tsx';
import baseClasses from '../../../shared-components/shared-styles.module.css';
import classes from './ContactUs.module.css';

const categories = [
  { label: 'An Error Report', value: 'error_report' },
  { label: 'An Idea', value: 'idea' },
  { label: 'A Testimonial', value: 'testimonial' },
  { label: 'Other', value: 'other' },
];

export function ContactUs() {
  const [isLoading, setIsLoading] = useState(false);
  const [turnstileToken, setTurnstileToken] = useState<string | null>(null);
  const [status, setStatus] = useState({ type: '', message: '' });
  const [rating, setRating] = useState(5);
  const [checked, setChecked] = useState(false);
  const auth = useAuth();

  const form = useForm({
    initialValues: {
      category: 'error_report',
      message: '',
    },
  });

  const mutation = useMutation({
    mutationFn: async (values: typeof form.values) => {
      setIsLoading(true);
      let data = {};
      if (values.category === 'testimonial') {
        data = { rating, consent: checked };
      }

      const requestBody: ContactUsRequest = {
        email: `${auth.user?.profile.email}`,
        name: `${auth.user?.profile.given_name} ${auth.user?.profile.family_name}`,
        message: values.message,
        token: turnstileToken!,
        user_id: auth.user?.profile.sub,
        category: values.category,
        data,
      };
      ContactUsService.contactUsSendMessage({ requestBody });

      setTimeout(() => {
        form.reset();
        setIsLoading(false);
        setStatus({
          type: 'Success',
          message: "Message sent successfully! We'll get back to you soon.",
        });
      }, 250);
    },
  });

  function getTextAreaPlaceholder(values: typeof form.values): string {
    if (values.category === 'idea') {
      return 'What feature would you like to see?';
    } else if (values.category === 'testimonial') {
      return 'Share your thoughts!';
    } else if (values.category === 'error_report') {
      return 'Please describe the issue with as much detail as you can';
    }
    return 'Share your thoughts or describe the issue...';
  }

  function hideTestimonialInputs(values: typeof form.values): boolean {
    return values.category !== 'testimonial';
  }

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <SimpleGrid cols={{ base: 1, sm: 2 }} spacing={50}>
            <div>
              <Title order={2} visibleFrom="sm">
                Send us a message
              </Title>
              <Title order={3} hiddenFrom="sm">
                Send us a message
              </Title>
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
                  color="green"
                  radius="md"
                  title={status.type}
                  icon={<IconInfoCircle />}
                  mb={10}
                  withCloseButton
                  onClose={() => setStatus({ type: '', message: '' })}
                >
                  {status.message}
                </Alert>
              )}
              <Group>
                <Text>This is</Text>
                <Select
                  data={categories}
                  key={form.key('category')}
                  defaultValue="error_report"
                  {...form.getInputProps('category')}
                  classNames={{ input: classes.input, label: classes.inputLabel }}
                  allowDeselect={false}
                  withAsterisk
                />
              </Group>
              <Group mb={30} gap="xs" display={hideTestimonialInputs(form.values) ? 'none' : ''}>
                <Title order={5} mt={15} c="var(--mantine-color-gray-7)">
                  Need ideas? Answer the following questions!
                </Title>
                <Text size="sm" c="var(--mantine-color-gray-7)">
                  • How did Fern Labour fit into your birth plan?
                </Text>
                <Text size="sm" c="var(--mantine-color-gray-7)">
                  • What advice would you give someone considering Fern Labour for their own
                  journey?
                </Text>
                <Text size="sm" c="var(--mantine-color-gray-7)">
                  • What was your favourite part of Fern Labour?
                </Text>
              </Group>
              <Rating
                defaultValue={5}
                size="lg"
                value={rating}
                onChange={setRating}
                display={hideTestimonialInputs(form.values) ? 'none' : ''}
              />
              <Textarea
                required
                key={form.key('message')}
                placeholder={getTextAreaPlaceholder(form.values)}
                minRows={5}
                maxRows={8}
                data-autofocus
                autosize
                mt="md"
                classNames={{ input: classes.input, label: classes.inputLabel }}
                {...form.getInputProps('message')}
              />
              <Checkbox
                mt={25}
                label="I give permission to use this testimonial across social channels and other marketing materials."
                checked={checked}
                onChange={(event) => setChecked(event.currentTarget.checked)}
                display={hideTestimonialInputs(form.values) ? 'none' : ''}
              />
              <Space h={20} />
              <Group align="center" justify="center" mt={10}>
                <Turnstile
                  sitekey={import.meta.env.VITE_CLOUDFLARE_SITEKEY || '1x00000000000000000000AA'}
                  onVerify={(token) => setTurnstileToken(token)}
                />
              </Group>
              <Group justify="flex-end" mt="md">
                <Button
                  type="submit"
                  className={classes.control}
                  radius="lg"
                  disabled={isLoading || status.type !== ''}
                >
                  {isLoading ? 'Sending...' : 'Submit'}
                </Button>
              </Group>
            </form>
          </SimpleGrid>
        </div>
      </div>
    </div>
  );
}
