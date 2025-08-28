import { useState } from 'react';
import { useApiAuth } from '@base/shared-components/hooks/useApiAuth.ts';
import { validateMessage } from '@base/shared-components/utils.tsx';
import { ContactUsService } from '@clients/contact_service/sdk.gen.ts';
import { ContactUsRequest } from '@clients/contact_service/types.gen.ts';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription.tsx';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle.tsx';
import { IconInfoCircle } from '@tabler/icons-react';
import { useMutation } from '@tanstack/react-query';
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
import { ContactIconsList } from './ContactIcons.tsx';
import classes from './ContactUs.module.css';
import baseClasses from '@shared/shared-styles.module.css';

const categories = [
  { label: 'An Error Report', value: 'error_report' },
  { label: 'An Idea', value: 'idea' },
  { label: 'A Testimonial', value: 'testimonial' },
  { label: 'Other', value: 'other' },
];

export function ContactUs() {
  const [isLoading, setIsLoading] = useState(false);
  const { user } = useApiAuth();
  const [turnstileToken, setTurnstileToken] = useState<string | null>(null);
  const [status, setStatus] = useState({ type: '', message: '' });
  const [rating, setRating] = useState(5);
  const [checked, setChecked] = useState(false);

  const form = useForm({
    initialValues: {
      category: 'error_report',
      message: '',
    },
    validate: { message: (message) => validateMessage(message) },
  });

  const mutation = useMutation({
    mutationFn: async (values: typeof form.values) => {
      setIsLoading(true);
      let data = {};
      if (values.category === 'testimonial') {
        data = { rating, consent: checked };
      }

      const requestBody: ContactUsRequest = {
        email: `${user?.profile.email}`,
        name: `${user?.profile.given_name} ${user?.profile.family_name}`,
        message: values.message,
        token: turnstileToken!,
        user_id: user?.profile.sub,
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

  const title = 'Send us a message';
  const description = 'Leave your email and we will get back to you within 24 hours';

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <SimpleGrid cols={{ base: 1, sm: 2 }} spacing={50}>
            <div>
              <ResponsiveTitle title={title} />
              <ResponsiveDescription description={description} marginTop={10} />
              <Space h="lg" />
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
                  classNames={{
                    input: baseClasses.input,
                    label: classes.inputLabel,
                    dropdown: baseClasses.selectDropdown,
                  }}
                  allowDeselect={false}
                  withAsterisk
                />
              </Group>
              <Group mb={30} gap="xs" display={hideTestimonialInputs(form.values) ? 'none' : ''}>
                <Title order={5} mt={15} className={baseClasses.description}>
                  Need ideas? Answer the following questions!
                </Title>
                <Text size="sm" className={baseClasses.description}>
                  • How did Fern Labour fit into your birth plan?
                </Text>
                <Text size="sm" className={baseClasses.description}>
                  • What advice would you give someone considering Fern Labour for their own
                  journey?
                </Text>
                <Text size="sm" className={baseClasses.description}>
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
                classNames={{ input: baseClasses.input, label: classes.inputLabel }}
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
                  color="var(--mantine-primary-color-4)"
                  variant="filled"
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
