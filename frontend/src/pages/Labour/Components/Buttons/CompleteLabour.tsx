import { Button, Tooltip } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { CompleteLabourRequest, LabourService, OpenAPI } from '../../../../client';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import ConfirmCompleteLabourModal from '../Modals/ConfirmCompleteLabour';

export default function CompleteLabourButton({labourNotes, disabled, setLabour}: {labourNotes: string, disabled: boolean, setLabour: Function}) {
    const auth = useAuth()
    const navigate = useNavigate();
    const [getConfimation, setGetConfimation] = useState(false);
    const [confirmedCompleteLabour, setConfirmedCompleteLabour] = useState(false);
    OpenAPI.TOKEN = async () => {
        return auth.user?.access_token || ""
    }

    const completeLabour = async () => {
        try {
            const requestBody: CompleteLabourRequest = {
                "end_time": new Date().toISOString(),
                "notes": labourNotes
            }
            const response = await LabourService.completeLabourApiV1LabourCompletePut(
                {requestBody:requestBody}
            )
            setLabour(response.labour);
            navigate("/");
        } catch (err) {
            console.error('Error completing labour:', err);
        }
    }
    if (getConfimation) {
        if (confirmedCompleteLabour) {
            completeLabour()
        } else {
            return <ConfirmCompleteLabourModal setGetConfirmation={setGetConfimation} setConfirmedComplete={setConfirmedCompleteLabour} />
        }
    }

    if (disabled) {
        return (
            <Tooltip label="End your current contraction first">
                <Button data-disabled size='xl' color='var(--mantine-color-pink-4)' radius="lg" variant="filled" onClick={(event) => event.preventDefault()}>
                    Complete Labour
                </Button>
            </Tooltip>
        )
    }
    return <Button size='xl' color='var(--mantine-color-pink-4)' radius="lg" variant="filled" onClick={() => setGetConfimation(true)}>Complete Labour</Button>;
}