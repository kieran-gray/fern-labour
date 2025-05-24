import { useCallback, useState } from 'react';
import { IconPencil, IconSend, IconSpeakerphone } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import _ from 'lodash';
import { useAuth } from 'react-oidc-context';
import { Button, SegmentedControl, TextInput } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
  LabourDTO,
  LabourUpdateDTO,
  LabourUpdateRequest,
  LabourUpdatesService,
  LabourUpdateType,
  OpenAPI,
} from '../../../../clients/labour_service';
import { useLabour } from '../../LabourContext';
import ConfirmAnnouncementModal from './ConfirmAnnouncement';
import classes from './LabourUpdates.module.css';

function createLabourUpdate(message: string, labourId: string | null, labourUpdateType: string) {
  const labourUpdate: LabourUpdateDTO = {
    id: 'placeholder',
    labour_update_type: labourUpdateType,
    message,
    labour_id: labourId || '',
    sent_time: new Date().toISOString(),
    edited: false,
    application_generated: false,
  };
  return labourUpdate;
}

export function LabourUpdateControls() {
  const [message, setMessage] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [labourUpdateType, setLabourUpdateType] = useState<LabourUpdateType>('status_update');
  const [mutationInProgress, setMutationInProgress] = useState(false);

  const auth = useAuth();
  const { labourId } = useLabour();
  const queryClient = useQueryClient();

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const handleMessageChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(event.currentTarget.value);
  }, []);

  const mutation = useMutation({
    mutationFn: async (labourUpdate: LabourUpdateDTO) => {
      setMutationInProgress(true);
      const requestBody: LabourUpdateRequest = {
        labour_update_type: labourUpdateType,
        sent_time: labourUpdate.sent_time,
        message: labourUpdate.message,
      };
      const response = await LabourUpdatesService.postLabourUpdate({ requestBody });
      return response.labour;
    },
    onMutate: async (labourUpdate: LabourUpdateDTO) => {
      await queryClient.cancelQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      const previousLabourState: LabourDTO | undefined = queryClient.getQueryData([
        'labour',
        auth.user?.profile.sub,
      ]);
      if (previousLabourState != null) {
        const newLabourState = _.cloneDeep(previousLabourState);
        newLabourState.labour_updates.push(labourUpdate);
        queryClient.setQueryData(['labour', auth.user?.profile.sub], newLabourState);
      }
      return { previousLabourState };
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
      setMessage('');
    },
    onError: (error, _, context) => {
      if (context != null) {
        queryClient.setQueryData(['labour', auth.user?.profile.sub], context.previousLabourState);
      }
      notifications.show({
        title: 'Error',
        message: `Error posting ${labourUpdateType === 'status_update' ? 'status update' : 'announcement'}: ${error.message}`,
        radius: 'lg',
        color: 'var(--mantine-color-primary-7)',
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      setMutationInProgress(false);
    },
  });

  const handleConfirm = () => {
    setIsModalOpen(false);
    mutation.mutate(createLabourUpdate(message, labourId, labourUpdateType));
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const handleSubmit = () => {
    if (labourUpdateType === 'announcement') {
      setIsModalOpen(true);
    } else {
      mutation.mutate(createLabourUpdate(message, labourId, labourUpdateType));
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
    color: 'var(--mantine-color-primary-4)',
    variant: 'filled',
    radius: 'xl',
    type: 'submit',
    disabled: !message,
    loading: mutationInProgress,
    className: classes.statusUpdateButton,
    onClick: handleSubmit,
    style: { minWidth: '200px' },
  };

  const inputIcon = <IconPencil size={18} stroke={1.5} />;

  const inputProps = {
    mt: 10,
    radius: 'lg',
    placeholder: "What's happening with your labour?",
    onChange: handleMessageChange,
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
        color="var(--mantine-color-primary-4)"
      />
      <TextInput {...inputProps} rightSection={inputIcon} size="md" visibleFrom="sm" />
      <TextInput {...inputProps} rightSection={inputIcon} size="sm" hiddenFrom="sm" />
      <div className={classes.flexRow} style={{ marginTop: '10px' }}>
        <Button {...buttonProps} type="submit" rightSection={buttonIcon} size="lg" visibleFrom="sm">
          {buttonText}
        </Button>
        <Button {...buttonProps} type="submit" rightSection={buttonIcon} size="md" hiddenFrom="sm">
          {buttonText}
        </Button>
      </div>
      {isModalOpen && (
        <ConfirmAnnouncementModal
          message={message}
          onConfirm={handleConfirm}
          onCancel={handleCancel}
        />
      )}
    </>
  );
}
