import { useState } from 'react';
import { IconClock, IconTrash, IconUpload } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button, Modal, Slider, Space, Text } from '@mantine/core';
import { TimeInput } from '@mantine/dates';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import {
  DeleteContractionRequest,
  LabourService,
  OpenAPI,
  UpdateContractionRequest,
} from '../../../../client';
import ConfirmActionModal from './ConfirmActionModal';
import { ContractionData } from './ContractionTimeline';
import modalClasses from '../../../../shared-components/Modal.module.css';
import classes from './Contractions.module.css';

type CloseFunctionType = (...args: any[]) => void;

export const EditContractionModal = ({
  contractionData,
  opened,
  close,
}: {
  contractionData: ContractionData;
  opened: boolean;
  close: CloseFunctionType;
}) => {
  const auth = useAuth();
  const [updateMutationInProgress, setUpdateMutationInProgress] = useState<boolean>(false);
  const [deleteMutationInProgress, setDeleteMutationInProgress] = useState<boolean>(false);
  const [getConfirmation, setGetConfirmation] = useState<boolean>(false);
  const [confirmed, setConfirmed] = useState<boolean>(false);
  const queryClient = useQueryClient();

  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      startTime: '',
      endTime: '',
      intensity: undefined,
    },
  });

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const updateTime = (dateTime: string, time: string) => {
    const split = dateTime.split('T');
    split[1] = `${time}Z`;
    return split.join('T');
  };

  const deleteContractionMutation = useMutation({
    mutationFn: async ({ contractionId }: { contractionId: string }) => {
      setDeleteMutationInProgress(true);
      const requestBody: DeleteContractionRequest = { contraction_id: contractionId };
      const response = await LabourService.deleteContraction({ requestBody });
      return response.labour;
    },
    onSuccess: async (labour) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
      setDeleteMutationInProgress(false);
      notifications.show({
        title: 'Success',
        message: `Contraction Deleted`,
        radius: 'lg',
        color: 'var(--mantine-color-green-3)',
      });
      close();
    },
    onError: async (_) => {
      setDeleteMutationInProgress(false);
      notifications.show({
        title: 'Error Deleting Contraction',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
    },
  });

  const updateContractionMutation = useMutation({
    mutationFn: async ({
      values,
      contractionId,
    }: {
      values: typeof form.values;
      contractionId: string;
    }) => {
      setUpdateMutationInProgress(true);
      const startTime =
        values.startTime !== ''
          ? updateTime(contractionData!.startTime, values.startTime)
          : contractionData!.startTime;
      const endTime =
        values.endTime !== ''
          ? updateTime(contractionData!.endTime, values.endTime)
          : contractionData!.endTime;

      const requestBody: UpdateContractionRequest = {
        start_time: startTime,
        end_time: endTime,
        intensity: values.intensity != null ? values.intensity : contractionData!.intensity,
        contraction_id: contractionId,
      };
      const response = await LabourService.updateContraction({ requestBody });
      return response.labour;
    },
    onSuccess: async (labour) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
      setUpdateMutationInProgress(false);
      notifications.show({
        title: 'Success',
        message: `Contraction Updated`,
        radius: 'lg',
        color: 'var(--mantine-color-green-3)',
      });
      close();
    },
    onError: async (_) => {
      setUpdateMutationInProgress(false);
      notifications.show({
        title: 'Error Updating Contraction',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
    },
    onSettled: () => {
      form.reset();
    },
  });

  if (getConfirmation) {
    if (confirmed) {
      deleteContractionMutation.mutate({ contractionId: contractionData!.contractionId });
      setGetConfirmation(false);
      setConfirmed(false);
    } else {
      return (
        <ConfirmActionModal setGetConfirmation={setGetConfirmation} setConfirmed={setConfirmed} />
      );
    }
  }

  const getTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString(navigator.language, {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    });
  };

  return (
    <Modal
      opened={opened}
      onClose={close}
      title="Update Contraction"
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
      <form
        onSubmit={form.onSubmit((values) =>
          updateContractionMutation.mutate({
            values,
            contractionId: contractionData!.contractionId,
          })
        )}
      >
        <Space h="lg" />
        <TimeInput
          rightSection={<IconClock />}
          withSeconds
          key={form.key('startTime')}
          radius="lg"
          label="Start Time"
          {...form.getInputProps('startTime')}
          defaultValue={getTime(contractionData?.startTime) || undefined}
        />
        <Space h="lg" />
        <TimeInput
          rightSection={<IconClock />}
          withSeconds
          key={form.key('endTime')}
          radius="lg"
          label="End Time"
          {...form.getInputProps('endTime')}
          defaultValue={getTime(contractionData?.endTime) || undefined}
        />
        <Space h="lg" />
        <Text size="sm" fw={500}>
          Intensity
        </Text>
        <Slider
          classNames={{
            root: classes.slider,
            markLabel: classes.markLabel,
            track: classes.track,
          }}
          color="var(--mantine-color-pink-4)"
          key={form.key('intensity')}
          size="xl"
          radius="lg"
          min={0}
          max={10}
          step={1}
          {...form.getInputProps('intensity')}
          defaultValue={contractionData?.intensity || undefined}
          marks={[
            { value: 0, label: '0' },
            { value: 5, label: 5 },
            { value: 10, label: 10 },
          ]}
        />
        <Space h="xl" />
        <div className={classes.flexRow}>
          <Button
            color="var(--mantine-color-pink-5)"
            leftSection={<IconTrash />}
            variant="filled"
            radius="xl"
            size="md"
            h={48}
            styles={{ section: { marginLeft: 20 } }}
            style={{ flexShrink: 1, marginRight: '5px' }}
            onClick={() => setGetConfirmation(true)}
            loading={deleteMutationInProgress}
          />
          <Button
            color="var(--mantine-color-pink-4)"
            leftSection={<IconUpload />}
            variant="light"
            radius="xl"
            size="md"
            h={48}
            styles={{ section: { marginRight: 22 } }}
            style={{ width: '100%' }}
            type="submit"
            loading={updateMutationInProgress}
          >
            Update Contraction
          </Button>
        </div>
      </form>
    </Modal>
  );
};
