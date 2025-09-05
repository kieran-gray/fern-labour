import { useState } from 'react';
import { UpdateContractionRequest } from '@clients/labour_service';
import { GenericConfirmModal } from '@shared/GenericConfirmModal/GenericConfirmModal';
import { useDeleteContraction, useUpdateContraction } from '@shared/hooks';
import { IconClock, IconTrash, IconUpload } from '@tabler/icons-react';
import { Button, Modal, Slider, Space, Text } from '@mantine/core';
import { TimeInput } from '@mantine/dates';
import { useForm } from '@mantine/form';
import { ContractionData } from './ContractionTimelineCustom';
import { updateTime } from './UpdateTime';
import classes from './Contractions.module.css';
import modalClasses from '@shared/Modal.module.css';

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
  const [isModalOpen, setIsModalOpen] = useState(false);

  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      startTime: '',
      endTime: '',
      intensity: undefined,
    },
  });

  const deleteContractionMutation = useDeleteContraction();
  const updateContractionMutation = useUpdateContraction();

  const handleDeleteContraction = (contractionId: string) => {
    deleteContractionMutation.mutate(contractionId, {
      onSuccess: () => {
        close();
      },
    });
  };

  const handleUpdateContraction = ({
    values,
    contractionId,
  }: {
    values: typeof form.values;
    contractionId: string;
  }) => {
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

    updateContractionMutation.mutate(requestBody, {
      onSuccess: () => {
        form.reset();
        close();
      },
    });
  };

  const handleConfirm = () => {
    setIsModalOpen(false);
    handleDeleteContraction(contractionData!.contractionId);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const getTime = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString(navigator.language, {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    });
  };

  return (
    <>
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
            handleUpdateContraction({
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
            classNames={{
              label: classes.timeInputLabel,
              input: classes.timeInput,
              section: classes.timeInputSection,
            }}
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
            classNames={{
              label: classes.timeInputLabel,
              input: classes.timeInput,
              section: classes.timeInputSection,
            }}
            defaultValue={getTime(contractionData?.endTime) || undefined}
          />
          <Space h="lg" />
          <Text
            size="sm"
            fw={500}
            c="light-dark(var(--mantine-color-gray-7), var(--mantine-color-gray-2))"
          >
            Intensity
          </Text>
          <Slider
            classNames={{
              root: classes.slider,
              markLabel: classes.markLabel,
              track: classes.track,
            }}
            color="var(--mantine-primary-color-4)"
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
              color="var(--mantine-primary-color-5)"
              leftSection={<IconTrash />}
              variant="filled"
              radius="xl"
              size="md"
              h={48}
              w={48}
              px={0}
              styles={{ section: { marginLeft: 10 } }}
              onClick={() => setIsModalOpen(true)}
              loading={deleteContractionMutation.isPending}
              aria-label="Delete contraction"
            />
            <Button
              color="var(--mantine-primary-color-4)"
              leftSection={<IconUpload />}
              variant="light"
              radius="xl"
              size="md"
              h={48}
              flex={1}
              ml="sm"
              type="submit"
              loading={updateContractionMutation.isPending}
            >
              Update
            </Button>
          </div>
        </form>
      </Modal>
      <GenericConfirmModal
        isOpen={isModalOpen}
        title="Delete Contraction?"
        confirmText="Delete"
        message="This can't be undone."
        onConfirm={handleConfirm}
        onCancel={handleCancel}
        isDangerous
      />
    </>
  );
};
