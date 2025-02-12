import { useState } from 'react';
import { IconSpeakerphone } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button, Tooltip } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { ApiError, LabourService, MakeAnnouncementRequest, OpenAPI } from '../../../../client';
import ConfirmAnnouncementModal from '../Modals/ConfirmAnnouncement';
import baseClasses from '../../../../shared-components/shared-styles.module.css';

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
      const requestBody: MakeAnnouncementRequest = {
        sent_time: new Date().toISOString(),
        message,
      };
      const response = await LabourService.makeAnnouncementApiV1LabourAnnouncementMakePost({
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
          color: 'var(--mantine-color-pink-9)',
          classNames: {
            title: baseClasses.notificationTitle,
            description: baseClasses.notificationDescription,
          },
          style: {
            backgroundColor: 'var(--mantine-color-pink-4)',
            color: 'var(--mantine-color-white)',
          },
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
  const icon = <IconSpeakerphone size={25} />;

  const button = (
    <Button
      leftSection={icon}
      radius="lg"
      size="xl"
      variant="outline"
      disabled={!message}
      onClick={() => {
        if (message !== '') {
          setGetConfimation(true);
        }
      }}
    >
      Announce
    </Button>
  );

  if (!message) {
    return <Tooltip label="Enter a message first">{button}</Tooltip>;
  }
  return button;
}
