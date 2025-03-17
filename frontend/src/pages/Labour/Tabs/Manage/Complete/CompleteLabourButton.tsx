import { useState } from 'react';
import { IconConfetti } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Button, Tooltip } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { CompleteLabourRequest, LabourService, OpenAPI } from '../../../../../client';
import { useLabour } from '../../../LabourContext';
import ConfirmCompleteLabourModal from './ConfirmCompleteLabour';

export default function CompleteLabourButton({
  labourNotes,
  disabled,
}: {
  labourNotes: string;
  disabled: boolean;
}) {
  const auth = useAuth();
  const navigate = useNavigate();
  const { setLabourId } = useLabour();
  const [getConfimation, setGetConfimation] = useState(false);
  const [confirmedCompleteLabour, setConfirmedCompleteLabour] = useState(false);
  const [isMutating, setIsMutating] = useState(false);
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (labourNotes: string) => {
      setIsMutating(true);
      const requestBody: CompleteLabourRequest = {
        end_time: new Date().toISOString(),
        notes: labourNotes,
      };
      await LabourService.completeLabourApiV1LabourCompletePut({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['birthingPerson', auth.user?.profile.sub] });
      queryClient.invalidateQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      setLabourId(null);
      navigate('/completed');
    },
    onError: (error) => {
      console.error('Error completing labour', error);
      notifications.show({
        title: 'Error Completing Labour',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
    },
    onSettled: () => {
      setIsMutating(false);
    },
  });

  if (getConfimation) {
    if (confirmedCompleteLabour) {
      mutation.mutate(labourNotes);
      setGetConfimation(false);
      setConfirmedCompleteLabour(false);
    } else {
      return (
        <ConfirmCompleteLabourModal
          setGetConfirmation={setGetConfimation}
          setConfirmedComplete={setConfirmedCompleteLabour}
        />
      );
    }
  }

  const icon = <IconConfetti size={25} />;

  if (disabled) {
    return (
      <Tooltip label="End your current contraction first">
        <Button
          data-disabled
          leftSection={icon}
          size="lg"
          color="var(--mantine-color-pink-4)"
          radius="xl"
          variant="filled"
          loading={isMutating}
          onClick={(event) => event.preventDefault()}
        >
          Complete Labour
        </Button>
      </Tooltip>
    );
  }
  return (
    <Button
      leftSection={icon}
      size="lg"
      color="var(--mantine-color-pink-4)"
      radius="xl"
      variant="filled"
      onClick={() => setGetConfimation(true)}
    >
      Complete Labour
    </Button>
  );
}
