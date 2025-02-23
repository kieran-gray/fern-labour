import { IconSend } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button, Tooltip } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { ApiError, LabourService, LabourUpdateRequest, OpenAPI } from '../../../../../client';

export function PostStatusUpdateButton({
  message,
  setUpdate,
}: {
  message: string;
  setUpdate: Function;
}) {
  const auth = useAuth();

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (message: string) => {
      const requestBody: LabourUpdateRequest = {
        labour_update_type: 'status_update',
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
      setUpdate('');
    },
    onError: (error) => {
      if (error instanceof ApiError) {
        notifications.show({
          title: 'Error',
          message: 'Something went wrong, please try again.',
          radius: 'lg',
          color: 'var(--mantine-color-pink-7)',
        });
      }
    },
  });

  const button = (
    <Button
      color="var(--mantine-color-pink-4)"
      rightSection={<IconSend size={18} stroke={1.5} />}
      variant="filled"
      radius="xl"
      size="md"
      h={48}
      style={{ minWidth: '200px' }}
      type="submit"
      disabled={!message}
      onClick={() => mutation.mutate(message)}
    >
      Post Update
    </Button>
  );

  if (!message) {
    return <Tooltip label="Enter a message first">{button}</Tooltip>;
  }
  return button;
}
