import { useState } from 'react';
import { IconCheck, IconLoader, IconSelector, IconUpload, IconX } from '@tabler/icons-react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useSearchParams } from 'react-router-dom';
import { Button, Modal, MultiSelect } from '@mantine/core';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import {
  OpenAPI,
  SubscriptionDTO,
  SubscriptionManagementService,
  UpdateContactMethodsRequest,
  UserService,
} from '../../../../client';
import { ImportantText } from '../../../../shared-components/ImportantText/ImportantText';
import { warnNonUKNumber, warnNoNumberSet } from './ContactMethods';
import modalClasses from '../../../../shared-components/Modal.module.css';
import classes from './ContactMethodsForm.module.css';

type CloseFunctionType = (...args: any[]) => void;

export default function ContactMethodsForm({
  subscription,
  opened,
  close,
}: {
  subscription: SubscriptionDTO;
  opened: boolean;
  close: CloseFunctionType;
}) {
  const auth = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();
  const prompt = searchParams.get('prompt');

  const defaultIcon = <IconUpload size={18} stroke={1.5} />;
  const [icon, setIcon] = useState<React.ReactNode>(defaultIcon);
  const [mutationInProgress, setMutationInProgress] = useState<boolean>(false);

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const { status, data } = useQuery({
    queryKey: ['subscriber', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await UserService.getUser();
        return response;
      } catch (err) {
        throw new Error('Failed to load subscriber. Please try again later.');
      }
    },
  });

  let contactMethodsWarning = null;
  if (status === 'success') {
    contactMethodsWarning =
      warnNoNumberSet(subscription.contact_methods, data.user.phone_number) ||
      warnNonUKNumber(subscription.contact_methods, data.user.phone_number);
  }

  const form = useForm({
    mode: 'controlled',
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
      const response = await SubscriptionManagementService.updateContactMethods({ requestBody });
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
      if (prompt === 'contactMethods') {
        searchParams.delete('prompt');
        setSearchParams(searchParams);
      }
      close();
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

  const options = [
    { value: 'whatsapp', label: 'WhatsApp', disabled: form.values.contactMethods.includes('sms') },
    { value: 'sms', label: 'Text', disabled: form.values.contactMethods.includes('whatsapp') },
    { value: 'email', label: 'Email' },
  ];

  return (
    <Modal
      opened={opened}
      closeOnClickOutside
      onClose={() => {
        searchParams.delete('prompt');
        setSearchParams(searchParams);
        close();
      }}
      title="Contact Methods"
      centered
      overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
      classNames={{
        content: modalClasses.modalRoot,
        header: modalClasses.modalHeader,
        title: modalClasses.modalTitle,
        body: modalClasses.modalBody,
        close: modalClasses.closeButton,
      }}
    >
      <div style={{ padding: '20px 10px 10px' }}>
        {contactMethodsWarning != null && (
          <div style={{ marginBottom: '20px' }}>
            <ImportantText message={contactMethodsWarning} />
          </div>
        )}

        <form
          onSubmit={form.onSubmit((values) =>
            mutation.mutate({ values, subscriptionId: subscription.id })
          )}
        >
          <div className={classes.flexColumn}>
            <MultiSelect
              rightSection={<IconSelector size={18} stroke={1.5} />}
              key={form.key('contactMethods')}
              placeholder="Select"
              label="Update your contact methods"
              description="How would you like to be notified about updates to this labour?"
              data={options}
              size="md"
              radius="xl"
              {...form.getInputProps('contactMethods')}
              classNames={{
                wrapper: classes.input,
                pill: classes.pill,
                description: classes.description,
                inputField: classes.input,
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
              visibleFrom="xs"
            >
              Update Contact Methods
            </Button>
            <Button
              color="var(--mantine-color-pink-4)"
              leftSection={icon}
              variant="outline"
              radius="xl"
              size="sm"
              h={48}
              className={classes.submitButton}
              styles={{ section: { marginRight: 22 } }}
              type="submit"
              loading={mutationInProgress}
              hiddenFrom="xs"
            >
              Update Contact Methods
            </Button>
          </div>
        </form>
      </div>
    </Modal>
  );
}
