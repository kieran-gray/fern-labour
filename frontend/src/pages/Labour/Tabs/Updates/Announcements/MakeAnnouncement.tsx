import { useState } from 'react';
import { IconSpeakerphone } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button, Tooltip } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { ApiError, LabourService, LabourUpdateRequest, OpenAPI } from '../../../../../client';
import ConfirmAnnouncementModal from './ConfirmAnnouncement';

export default function MakeAnnouncementButton({
  message,
  setAnnouncement,
}: {
  message: string;
  setAnnouncement: Function;
}) {
  const [getConfimation, setGetConfimation] = useState(false);
  const [confirmedMakeAnnouncement, setConfirmedMakeAnnouncement] = useState(false);
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (message: string) => {
      const requestBody: LabourUpdateRequest = {
        labour_update_type: 'announcement',
        sent_time: new Date().toISOString(),
        message,
      };
      const response = await LabourService.postLabourUpdateApiV1LabourLabourUpdatePost({
        requestBody,
      });
      return response.labour;
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
      setAnnouncement('');
    },
    onError: (error) => {
      if (error instanceof ApiError) {
        notifications.show({
          title: 'Error',
          message: 'Wait at least 10 seconds between announcements',
          radius: 'lg',
          color: 'var(--mantine-color-pink-7)',
        });
      }
    },
  });

  if (getConfimation) {
    if (confirmedMakeAnnouncement) {
      setGetConfimation(false);
      setConfirmedMakeAnnouncement(false);
      mutation.mutate(message);
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
      rightSection={<IconSpeakerphone size={22} stroke={1.5} />}
      radius="xl"
      size="lg"
      color="var(--mantine-color-pink-4)"
      variant="filled"
      style={{ minWidth: '200px' }}
      disabled={!message}
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
