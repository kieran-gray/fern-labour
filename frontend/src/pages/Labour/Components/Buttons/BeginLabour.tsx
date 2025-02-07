import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button } from '@mantine/core';
import { BeginLabourRequest, LabourService, OpenAPI } from '../../../../client';

export default function BeginLabourButton() {
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: async () => {
      const requestBody: BeginLabourRequest = { first_labour: true }; // TODO make this not constant
      const response = await LabourService.beginLabourApiV1LabourBeginPost({
        requestBody,
      });
      return response.labour;
    },
    onSuccess: (labour) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
    },
    onError: (error) => {
      console.error('Error starting labour', error);
    },
  });
  return (
    <Button
      size="lg"
      radius="lg"
      color="var(--mantine-color-pink-4)"
      variant="filled"
      onClick={() => mutation.mutate()}
      style={{ flex: 1 }}
    >
      Begin Labour
    </Button>
  );
}
