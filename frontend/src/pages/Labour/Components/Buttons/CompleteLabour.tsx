import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Button, Tooltip } from '@mantine/core';
import { CompleteLabourRequest, LabourService, OpenAPI } from '../../../../client';
import ConfirmCompleteLabourModal from '../Modals/ConfirmCompleteLabour';

export default function CompleteLabourButton({
  labourNotes,
  disabled,
}: {
  labourNotes: string;
  disabled: boolean;
}) {
  const auth = useAuth();
  const navigate = useNavigate();
  const [getConfimation, setGetConfimation] = useState(false);
  const [confirmedCompleteLabour, setConfirmedCompleteLabour] = useState(false);
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (labourNotes: string) => {
      const requestBody: CompleteLabourRequest = {
        end_time: new Date().toISOString(),
        notes: labourNotes,
      };
      await LabourService.completeLabourApiV1LabourCompletePut({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['birthingPerson', auth.user?.profile.sub] });
      queryClient.invalidateQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      navigate('/');
    },
    onError: (error) => {
      console.error('Error completing labour', error);
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

  if (disabled) {
    return (
      <Tooltip label="End your current contraction first">
        <Button
          data-disabled
          size="xl"
          color="var(--mantine-color-pink-4)"
          radius="lg"
          variant="filled"
          onClick={(event) => event.preventDefault()}
        >
          Complete Labour
        </Button>
      </Tooltip>
    );
  }
  return (
    <Button
      size="xl"
      color="var(--mantine-color-pink-4)"
      radius="lg"
      variant="filled"
      onClick={() => setGetConfimation(true)}
    >
      Complete Labour
    </Button>
  );
}
