import { useCallback, useState } from 'react';
import { LABOUR_UPDATE_MAX_LENGTH } from '@base/lib/constants';
import { useNetworkState } from '@base/offline/hooks';
import { useLabourV2Client, usePostLabourUpdateV2 } from '@shared/hooks';
import { IconPencil, IconSend, IconSpeakerphone, IconWifiOff } from '@tabler/icons-react';
import { Button, SegmentedControl, Text, Textarea } from '@mantine/core';
import ConfirmAnnouncementModal from './Modals/ConfirmAnnouncement';
import classes from './LabourUpdates.module.css';
import baseClasses from '@shared/shared-styles.module.css';
import { useLabour } from '@base/contexts/LabourContext';
import { LabourUpdateType } from '@base/clients/labour_service_v2';

export function LabourUpdateControls() {
  const [message, setMessage] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [labourUpdateType, setLabourUpdateType] = useState<LabourUpdateType>(LabourUpdateType.STATUS_UPDATE);
  const { labourId } = useLabour();
  const { isOnline } = useNetworkState();

  const client = useLabourV2Client();
  const mutation = usePostLabourUpdateV2(client);

  const handleMessageChange = useCallback((event: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (event.currentTarget.value.length <= LABOUR_UPDATE_MAX_LENGTH) {
      setMessage(event.currentTarget.value);
    }
  }, []);

  const handleSubmitUpdate = (updateType: LabourUpdateType, message: string) => {
    mutation.mutate(
      {
        labourId: labourId!,
        updateType,
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
    if (labourUpdateType === 'ANNOUNCEMENT') {
      setIsModalOpen(true);
    } else {
      handleSubmitUpdate(labourUpdateType, message);
    }
  };

  if (!isOnline) {
    return (
      <>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <IconWifiOff size={18} color="var(--mantine-primary-color-7)" />
          <Text size="sm" fw={500} className={baseClasses.description}>
            You are offline. Labour updates cannot be posted in offline mode.
          </Text>
        </div>
      </>
    );
  }

  const buttonIcon =
    labourUpdateType === 'STATUS_UPDATE' ? (
      <IconSend size={18} stroke={1.5} />
    ) : (
      <IconSpeakerphone size={18} stroke={1.5} />
    );

  const buttonText =
    labourUpdateType === 'STATUS_UPDATE' ? 'Post Status Update' : 'Make Announcement';

  const buttonProps = {
    variant: 'filled',
    radius: 'xl',
    type: 'submit',
    disabled: !message,
    loading: mutation.isPending,
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
          { label: 'Status Update', value: 'STATUS_UPDATE' },
          { label: 'Announcement', value: 'ANNOUNCEMENT' },
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
