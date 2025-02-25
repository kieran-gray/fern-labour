import { useState } from 'react';
import {
  IconCheck,
  IconInfoCircle,
  IconLoader,
  IconSelector,
  IconUpload,
  IconX,
} from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button, MultiSelect } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import {
  OpenAPI,
  SubscriptionDTO,
  SubscriptionManagementService,
  UpdateContactMethodsRequest,
} from '../../../../client';
import { ContainerHeader } from '../../../../shared-components/ContainerHeader/ContainerHeader';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './ContactMethodsForm.module.css';

export default function ContactMethodsForm({ subscription }: { subscription: SubscriptionDTO }) {
  const auth = useAuth();

  const defaultIcon = <IconUpload size={18} stroke={1.5} />;
  const [icon, setIcon] = useState<React.ReactNode>(defaultIcon);
  const [mutationInProgress, setMutationInProgress] = useState<boolean>(false);

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      contactMethods: subscription.contact_methods,
    },
  });

  const mutation = useMutation({
    mutationFn: async ({
      values,
      subscriptionId,
    }: {
      values: typeof form.values;
      subscriptionId: string;
    }) => {
      setMutationInProgress(true);
      setIcon(<IconLoader size={18} stroke={1.5} />);
      const requestBody: UpdateContactMethodsRequest = {
        contact_methods: values.contactMethods,
        subscription_id: subscriptionId,
      };
      const response =
        await SubscriptionManagementService.updateContactMethodsApiV1SubscriptionManagementUpdateContactMethodsPut(
          { requestBody }
        );
      return response.subscription;
    },
    onSuccess: async (subscription) => {
      queryClient.invalidateQueries({
        queryKey: ['subscription_data', subscription.id, auth.user?.profile.sub],
      });
      queryClient.invalidateQueries({
        queryKey: ['subscriber_subscriptions', auth.user?.profile.sub],
      });
      queryClient.setQueryData(
        ['subscription', subscription.id, auth.user?.profile.sub],
        subscription
      );
      setMutationInProgress(false);
      setIcon(<IconCheck size={18} stroke={1.5} />);
    },
    onError: async (error) => {
      setMutationInProgress(false);
      setIcon(<IconX size={18} stroke={1.5} />);
      notifications.show({
        title: 'Error Updating Contact Methods',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
      console.error('Error updating contact methods', error);
    },
    onSettled: async () => {
      await new Promise((r) => setTimeout(r, 1000));
      setIcon(defaultIcon);
    },
  });

  return (
    <div className={baseClasses.root}>
      <ContainerHeader title="Contact Methods" />
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            {subscription.contact_methods.length === 0 && (
              <div className={baseClasses.importantText} style={{ marginBottom: '20px' }}>
                <IconInfoCircle style={{ alignSelf: 'center', marginRight: '10px' }} />
                You will only receive live notifications if you add your preferred methods below
              </div>
            )}

            <form
              onSubmit={form.onSubmit((values) =>
                mutation.mutate({ values, subscriptionId: subscription.id })
              )}
            >
              <div className={classes.submitRow}>
                <MultiSelect
                  rightSection={<IconSelector size={18} stroke={1.5} />}
                  key={form.key('contactMethods')}
                  placeholder="Pick value"
                  label="Update your contact methods"
                  description="How would you like to be notified about updates to this labour?"
                  data={[
                    { value: 'sms', label: 'Text' },
                    { value: 'email', label: 'Email' },
                  ]}
                  size="md"
                  radius="xl"
                  {...form.getInputProps('contactMethods')}
                  classNames={{
                    wrapper: classes.input,
                    pill: classes.pill,
                    description: classes.description,
                  }}
                  comboboxProps={{
                    transitionProps: { transition: 'pop', duration: 200 },
                    shadow: 'md',
                  }}
                  clearable
                />
                <Button
                  color="var(--mantine-color-pink-4)"
                  leftSection={icon}
                  variant="outline"
                  radius="xl"
                  size="md"
                  h={48}
                  className={classes.submitButton}
                  styles={{ section: { marginRight: 22 } }}
                  type="submit"
                  loading={mutationInProgress}
                >
                  Update Contact Methods
                </Button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
