import { SubscriptionDTO, UpdateContactMethodsRequest } from '@clients/labour_service';
import { useUpdateContactMethods } from '@shared/hooks';
import { IconSelector, IconUpload } from '@tabler/icons-react';
import { useSearchParams } from 'react-router-dom';
import { Button, Modal, MultiSelect } from '@mantine/core';
import { useForm } from '@mantine/form';
import classes from './ContactMethodsForm.module.css';
import modalClasses from '@shared/Modal.module.css';

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
  const [searchParams, setSearchParams] = useSearchParams();
  const prompt = searchParams.get('prompt');

  const defaultIcon = <IconUpload size={18} stroke={1.5} />;

  const form = useForm({
    mode: 'controlled',
    initialValues: {
      contactMethods: subscription.contact_methods,
    },
  });

  const updateContactMethodsMutation = useUpdateContactMethods();
  const handleUpdateContactMethods = (values: typeof form.values) => {
    const requestBody: UpdateContactMethodsRequest = {
      contact_methods: values.contactMethods,
      subscription_id: subscription.id,
    };
    updateContactMethodsMutation.mutate(requestBody, {
      onSuccess: () => {
        if (prompt === 'contactMethods') {
          searchParams.delete('prompt');
          setSearchParams(searchParams);
        }
        close();
      },
    });
  };

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
        <form onSubmit={form.onSubmit((values) => handleUpdateContactMethods(values))}>
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
                options: classes.options,
                label: classes.label,
              }}
              comboboxProps={{
                transitionProps: { transition: 'pop', duration: 200 },
                shadow: 'md',
              }}
              clearable
            />
            <Button
              color="var(--mantine-primary-color-4)"
              leftSection={defaultIcon}
              variant="outline"
              radius="xl"
              size="md"
              h={48}
              className={classes.submitButton}
              styles={{ section: { marginRight: 22 } }}
              type="submit"
              loading={updateContactMethodsMutation.isPending}
              visibleFrom="xs"
            >
              Update Contact Methods
            </Button>
            <Button
              color="var(--mantine-primary-color-4)"
              leftSection={defaultIcon}
              variant="outline"
              radius="xl"
              size="sm"
              h={48}
              className={classes.submitButton}
              styles={{ section: { marginRight: 22 } }}
              type="submit"
              loading={updateContactMethodsMutation.isPending}
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
