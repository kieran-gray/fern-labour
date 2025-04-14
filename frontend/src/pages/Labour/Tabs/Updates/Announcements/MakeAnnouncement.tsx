import { useState } from 'react';
import { IconSpeakerphone } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import _ from 'lodash';
import { useAuth } from 'react-oidc-context';
import { Button, Tooltip } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
  ApiError,
  LabourDTO,
  LabourUpdateDTO,
  LabourUpdateRequest,
  LabourUpdatesService,
  OpenAPI,
} from '../../../../../client';
import { useLabour } from '../../../LabourContext';
import ConfirmAnnouncementModal from './ConfirmAnnouncement';

export default function MakeAnnouncementButton({
  message,
  setAnnouncement,
}: {
  message: string;
  setAnnouncement: Function;
}) {
  const [getConfimation, setGetConfimation] = useState(false);
  const [mutationInProgress, setMutationInProgress] = useState(false);
  const [confirmedMakeAnnouncement, setConfirmedMakeAnnouncement] = useState(false);
  const { labourId } = useLabour();

  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const queryClient = useQueryClient();

  const createLabourUpdate = (message: string) => {
    const labourUpdate: LabourUpdateDTO = {
      id: 'placeholder',
      labour_update_type: 'announcement',
      message,
      labour_id: labourId || '',
      sent_time: new Date().toISOString(),
    };
    return labourUpdate;
  };

  const mutation = useMutation({
    mutationFn: async (labourUpdate: LabourUpdateDTO) => {
      setMutationInProgress(true);
      const requestBody: LabourUpdateRequest = {
        labour_update_type: 'announcement',
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
        newLabourState.announcements.push(labourUpdate);
        queryClient.setQueryData(['labour', auth.user?.profile.sub], newLabourState);
      }
      return { previousLabourState };
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
      setAnnouncement('');
    },
    onError: (error, _, context) => {
      if (context != null) {
        queryClient.setQueryData(['labour', auth.user?.profile.sub], context.previousLabourState);
      }
      if (error instanceof ApiError) {
        notifications.show({
          title: 'Error',
          message: 'Wait at least 10 seconds between announcements',
          radius: 'lg',
          color: 'var(--mantine-color-pink-7)',
        });
      } else {
        notifications.show({
          title: 'Error making announcement',
          message: 'Something went wrong. Please try again.',
          radius: 'lg',
          color: 'var(--mantine-color-pink-7)',
        });
      }
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      setMutationInProgress(false);
    },
  });

  if (getConfimation) {
    if (confirmedMakeAnnouncement) {
      setGetConfimation(false);
      setConfirmedMakeAnnouncement(false);
      mutation.mutate(createLabourUpdate(message));
    } else {
      return (
        <ConfirmAnnouncementModal
          message={message}
          setGetConfirmation={setGetConfimation}
          setConfirmedComplete={setConfirmedMakeAnnouncement}
        />
      );
    }
  }

  const button = (
    <Button
      rightSection={<IconSpeakerphone size={18} stroke={1.5} />}
      radius="xl"
      size="lg"
      color="var(--mantine-color-pink-4)"
      variant="filled"
      style={{ minWidth: '200px' }}
      disabled={!message}
      loading={mutationInProgress}
      onClick={() => {
        if (message !== '') {
          setGetConfimation(true);
        }
      }}
    >
      Make Announcement
    </Button>
  );

  if (!message) {
    return <Tooltip label="Enter a message first">{button}</Tooltip>;
  }
  return button;
}
