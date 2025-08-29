import { useCallback, useState } from 'react';
import { LABOUR_UPDATE_MAX_LENGTH } from '@base/constants';
import { LabourUpdateType } from '@clients/labour_service';
import { useCreateLabourUpdate } from '@shared/hooks';
import { IconPencil, IconSend, IconSpeakerphone } from '@tabler/icons-react';
import { Button, SegmentedControl, Textarea } from '@mantine/core';
import ConfirmAnnouncementModal from './Modals/ConfirmAnnouncement';
import classes from './LabourUpdates.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export function LabourUpdateControls() {
  const [message, setMessage] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [labourUpdateType, setLabourUpdateType] = useState<LabourUpdateType>('status_update');

  const createLabourUpdateMutation = useCreateLabourUpdate();

  const handleMessageChange = useCallback((event: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (event.currentTarget.value.length <= LABOUR_UPDATE_MAX_LENGTH) {
      setMessage(event.currentTarget.value);
    }
  }, []);

  const handleSubmitUpdate = (labourUpdateType: LabourUpdateType, message: string) => {
    createLabourUpdateMutation.mutate(
      {
        labour_update_type: labourUpdateType,
        message,
      },
      {
        onSuccess: () => {
          setMessage('');
        },
      }
    );
  };
  const handleConfirm = () => {
    setIsModalOpen(false);
    handleSubmitUpdate(labourUpdateType, message);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const handleSubmit = () => {
    if (labourUpdateType === 'announcement') {
      setIsModalOpen(true);
    } else {
      handleSubmitUpdate(labourUpdateType, message);
    }
  };

  const buttonIcon =
    labourUpdateType === 'status_update' ? (
      <IconSend size={18} stroke={1.5} />
    ) : (
      <IconSpeakerphone size={18} stroke={1.5} />
    );

  const buttonText =
    labourUpdateType === 'status_update' ? 'Post Status Update' : 'Make Announcement';

  const buttonProps = {
    variant: 'filled',
    radius: 'xl',
    type: 'submit',
    disabled: !message,
    loading: createLabourUpdateMutation.isPending,
    className: classes.statusUpdateButton,
    onClick: handleSubmit,
    style: { minWidth: '200px' },
  };

  const inputIcon = <IconPencil size={18} stroke={1.5} />;

  const inputProps = {
    mt: 10,
    radius: 'lg',
    placeholder: "What's happening with your labour?",
    value: message,
  };

  return (
    <>
      <SegmentedControl
        value={labourUpdateType}
        onChange={(value: any) => setLabourUpdateType(value)}
        transitionTimingFunction="ease"
        fullWidth
        data={[
          { label: 'Status Update', value: 'status_update' },
          { label: 'Announcement', value: 'announcement' },
        ]}
        radius="lg"
        mt={20}
        color="var(--mantine-primary-color-4)"
      />
      <Textarea
        {...inputProps}
        rightSection={inputIcon}
        size="md"
        visibleFrom="sm"
        classNames={{
          description: baseClasses.description,
          input: baseClasses.input,
          section: baseClasses.section,
        }}
        onChange={handleMessageChange}
      />
      <Textarea
        {...inputProps}
        rightSection={inputIcon}
        size="sm"
        hiddenFrom="sm"
        classNames={{
          description: baseClasses.description,
          input: baseClasses.input,
          section: baseClasses.section,
        }}
        onChange={handleMessageChange}
      />
      <div className={classes.flexRow} style={{ marginTop: '10px' }}>
        <Button
          {...buttonProps}
          type="submit"
          rightSection={buttonIcon}
          size="lg"
          visibleFrom="sm"
          color="var(--mantine-primary-color-4)"
        >
          {buttonText}
        </Button>
        <Button
          {...buttonProps}
          type="submit"
          rightSection={buttonIcon}
          size="md"
          hiddenFrom="sm"
          color="var(--mantine-primary-color-4)"
        >
          {buttonText}
        </Button>
      </div>
      <ConfirmAnnouncementModal
        message={message}
        onConfirm={handleConfirm}
        onCancel={handleCancel}
        opened={isModalOpen}
      />
    </>
  );
}
