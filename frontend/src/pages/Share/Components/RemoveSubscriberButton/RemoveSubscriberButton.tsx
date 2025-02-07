import { useState } from 'react';
import { IconCircleMinus } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button } from '@mantine/core';
import { BirthingPersonService, OpenAPI, RemoveSubscriberRequest } from '../../../../client';
import ConfirmRemoveSubscriberModal from '../ConfirmRemoveSubscriberModal/ConfirmRemoveSubscriberModal';

export function RemoveSubscriberButton({ subscriber_id }: { subscriber_id: string }) {
  const [getConfimation, setGetConfimation] = useState(false);
  const [confirmed, setConfirmed] = useState(false);
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async () => {
      const requestBody: RemoveSubscriberRequest = { subscriber_id };
      await BirthingPersonService.removeSubscriberApiV1BirthingPersonRemoveSubscriberPost({
        requestBody,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscribers', auth.user?.profile.sub] });
    },
    onError: (error) => {
      console.error('Error removing subscriber', error);
    },
  });

  if (getConfimation) {
    if (confirmed) {
      mutation.mutate();
      setGetConfimation(false);
      setConfirmed(false);
    } else {
      return (
        <ConfirmRemoveSubscriberModal
          setGetConfirmation={setGetConfimation}
          setConfirmed={setConfirmed}
        />
      );
    }
  }

  return (
    <Button
      color="var(--mantine-color-pink-4)"
      variant="filled"
      rightSection={<IconCircleMinus size={20} stroke={1.5} />}
      radius="xl"
      size="md"
      pr={14}
      h={32}
      styles={{ section: { marginLeft: 22 } }}
      type="submit"
      onClick={() => setGetConfimation(true)}
    >
      Remove
    </Button>
  );
}
