import { Button } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { LabourService, MakeAnnouncementRequest, OpenAPI } from '../../../../client';
import { IconSpeakerphone } from '@tabler/icons-react';
import { useState } from 'react';
import ConfirmAnnouncementModal from '../Modals/ConfirmAnnouncement';

export default function MakeAnnouncementButton(
    {message, setLabour }: {message: string, setLabour: Function}
) {
    const [getConfimation, setGetConfimation] = useState(false);
    const [confirmedMakeAnnouncement, setConfirmedMakeAnnouncement] = useState(false);
    const auth = useAuth()
    OpenAPI.TOKEN = async () => {
        return auth.user?.access_token || ""
    }
    const makeAnnouncement = async () => {
        try {
            const sent_time = new Date().toISOString()
            const requestBody: MakeAnnouncementRequest = {
                "message": message,
                "sent_time": sent_time
            }
            const response = await LabourService.makeAnnouncementApiV1LabourAnnouncementMakePost(
                {requestBody:requestBody}
            )
            setLabour(response.labour);
        } catch (err) {
            console.error('Error making announcement', err);
        }
    }

    if (getConfimation) {
        if (confirmedMakeAnnouncement) {
            makeAnnouncement();
            setGetConfimation(false);
            setConfirmedMakeAnnouncement(false);
        } else {
            return <ConfirmAnnouncementModal message={message} setGetConfirmation={setGetConfimation} setConfirmedComplete={setConfirmedMakeAnnouncement} />
        }
    }

    
    const icon = <IconSpeakerphone size={25} />;
    return <Button leftSection={icon} radius="lg" size='xl' variant="outline" onClick={() => {if(message !== "") {setGetConfimation(true)}}}>Announce</Button>;
}