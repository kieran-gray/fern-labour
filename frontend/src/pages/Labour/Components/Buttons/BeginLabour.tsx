import { Button } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { BeginLabourRequest, LabourService, OpenAPI } from '../../../../client';
import { useMutation, useQueryClient } from '@tanstack/react-query';

export default function BeginLabourButton() {
    const auth = useAuth()
    OpenAPI.TOKEN = async () => {
        return auth.user?.access_token || ""
    }
    const queryClient = useQueryClient();

    const mutation = useMutation({
        mutationFn: async () => {
            const requestBody: BeginLabourRequest = {"first_labour": true} // TODO make this not constant
            const response = await LabourService.beginLabourApiV1LabourBeginPost(
                {requestBody: requestBody}
            )
            return response.labour
        },
        onSuccess: (labour) => {
          queryClient.setQueryData(['labour', auth.user?.profile.sub], labour)
        },
        onError: (error) => {
          console.error("Error starting labour", error)
        }
    });
    return <Button
        size="lg"
        radius="lg"
        color='var(--mantine-color-pink-4)'
        variant="filled"
        onClick={() => mutation.mutate()}
    >
        Begin Labour
    </Button>;
}