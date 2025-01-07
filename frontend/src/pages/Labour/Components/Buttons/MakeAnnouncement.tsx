import { Button } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { LabourService, MakeAnnouncementRequest, OpenAPI } from '../../../../client';
import { IconSpeakerphone } from '@tabler/icons-react';
import { useState } from 'react';
import ConfirmAnnouncementModal from '../Modals/ConfirmAnnouncement';
import { useMutation, useQueryClient } from '@tanstack/react-query';

export default function MakeAnnouncementButton({message, setAnnouncement}: {message: string, setAnnouncement: Function}) {
    const [getConfimation, setGetConfimation] = useState(false);
    const [confirmedMakeAnnouncement, setConfirmedMakeAnnouncement] = useState(false);
    const auth = useAuth()
    OpenAPI.TOKEN = async () => {
        return auth.user?.access_token || ""
    }
        
    const queryClient = useQueryClient();

    const mutation = useMutation({
        mutationFn: async (message: string) => {
            const requestBody: MakeAnnouncementRequest = {
                "sent_time": new Date().toISOString(),
                "message": message,
            }
            const response = await LabourService.makeAnnouncementApiV1LabourAnnouncementMakePost(
                {requestBody: requestBody}
            )
            return response.labour
        },
        onSuccess: (labour) => {
          queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
          setAnnouncement("")
        },
        onError: (error) => {
          console.error("Error making announcement", error)
        }
    });

    if (getConfimation) {
        if (confirmedMakeAnnouncement) {
            mutation.mutate(message);
            setGetConfimation(false);
            setConfirmedMakeAnnouncement(false);
        } else {
            return <ConfirmAnnouncementModal 
                message={message}
                setGetConfirmation={setGetConfimation}
                setConfirmedComplete={setConfirmedMakeAnnouncement}
            />
        }
    }

    
    const icon = <IconSpeakerphone size={25} />;
    return <Button
        leftSection={icon}
        radius="lg"
        size='xl'
        variant="outline"
        onClick={() => {if(message !== "") {setGetConfimation(true)}}}
    >
        Announce
    </Button>;
}