import { useState } from 'react';
import { Error } from '@base/shared-components/Notifications';
import { CompleteLabourRequest, LabourService } from '@clients/labour_service';
import { useLabour } from '@labour/LabourContext';
import { useApiAuth } from '@shared/hooks/useApiAuth';
import { IconConfetti } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { Button, Tooltip } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import ConfirmCompleteLabourModal from './ConfirmCompleteLabour';

export default function CompleteLabourButton({
  labourNotes,
  disabled,
}: {
  labourNotes: string;
  disabled: boolean;
}) {
  const { user } = useApiAuth();
  const navigate = useNavigate();
  const { setLabourId } = useLabour();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isMutating, setIsMutating] = useState(false);
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async (labourNotes: string) => {
      setIsMutating(true);
      const requestBody: CompleteLabourRequest = {
        end_time: new Date().toISOString(),
        notes: labourNotes,
      };
      await LabourService.completeLabour({ requestBody });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['birthingPerson', user?.profile.sub] });
      queryClient.invalidateQueries({ queryKey: ['labour', user?.profile.sub] });
      setLabourId(null);
      navigate('/completed');
    },
    onError: (error) => {
      console.error('Error completing labour', error);
      notifications.show({
        ...Error,
        title: 'Error Completing Labour',
        message: 'Something went wrong. Please try again.',
      });
    },
    onSettled: () => {
      setIsMutating(false);
    },
  });

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const handleConfirm = () => {
    setIsModalOpen(false);
    mutation.mutate(labourNotes);
  };

  const icon = <IconConfetti size={25} />;

  if (disabled) {
    return (
      <Tooltip
        label="End your current contraction first"
        events={{ hover: true, focus: false, touch: true }}
      >
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
    <>
      <Button
        leftSection={icon}
        size="lg"
        color="var(--mantine-color-pink-4)"
        radius="xl"
        variant="filled"
        onClick={() => setIsModalOpen(true)}
      >
        Complete Labour
      </Button>
      {isModalOpen && (
        <ConfirmCompleteLabourModal onConfirm={handleConfirm} onCancel={handleCancel} />
      )}
    </>
  );
}
