import { useState } from 'react';
import { IconSend } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import _ from 'lodash';
import { useAuth } from 'react-oidc-context';
import { Button } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import {
  LabourDTO,
  LabourUpdateDTO,
  LabourUpdateRequest,
  LabourUpdatesService,
  OpenAPI,
} from '../../../../client';
import { useLabour } from '../../LabourContext';
import classes from './LabourUpdates.module.css';

export function PostStatusUpdateButton({
  message,
  setUpdate,
}: {
  message: string;
  setUpdate: Function;
}) {
  const [mutationInProgress, setMutationInProgress] = useState(false);
  const auth = useAuth();
  const { labourId } = useLabour();

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const queryClient = useQueryClient();

  const createLabourUpdate = (message: string) => {
    const labourUpdate: LabourUpdateDTO = {
      id: 'placeholder',
      labour_update_type: 'status_update',
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
        labour_update_type: 'status_update',
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
      setUpdate('');
    },
    onError: (error, _, context) => {
      if (context != null) {
        queryClient.setQueryData(['labour', auth.user?.profile.sub], context.previousLabourState);
      }
      notifications.show({
        title: 'Error',
        message: `Error posting status update: ${error.message}`,
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      setMutationInProgress(false);
    },
  });

  return (
    <>
      <Button
        color="var(--mantine-color-pink-4)"
        rightSection={<IconSend size={18} stroke={1.5} />}
        variant="filled"
        radius="xl"
        size="lg"
        style={{ minWidth: '200px' }}
        type="submit"
        visibleFrom="sm"
        disabled={!message}
        loading={mutationInProgress}
        className={classes.statusUpdateButton}
        onClick={() => mutation.mutate(createLabourUpdate(message))}
      >
        Post Status Update
      </Button>
      <Button
        color="var(--mantine-color-pink-4)"
        rightSection={<IconSend size={18} stroke={1.5} />}
        variant="filled"
        radius="xl"
        size="md"
        hiddenFrom="sm"
        style={{ minWidth: '200px' }}
        type="submit"
        disabled={!message}
        loading={mutationInProgress}
        className={classes.statusUpdateButton}
        onClick={() => mutation.mutate(createLabourUpdate(message))}
      >
        Post Status Update
      </Button>
    </>
  );
}
