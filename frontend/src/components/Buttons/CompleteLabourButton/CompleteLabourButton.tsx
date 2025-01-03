import { Button, Tooltip } from '@mantine/core';
import { useAuth } from 'react-oidc-context';
import { CompleteLabourRequest, LabourResponse } from '../../../client';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import ConfirmCompleteLabourModal from '../../ConfirmCompleteLabourModal/ConfirmCompleteLabourModal';

export default function CompleteLabourButton({labourNotes, disabled, setLabour}: {labourNotes: string, disabled: boolean, setLabour: Function}) {
    const auth = useAuth()
    const navigate = useNavigate();
    const [completeClicked, setCompleteClicked] = useState(false);
    const [confirmedCompleteLabour, setConfirmedCompleteLabour] = useState(false);

    const completeLabour = async () => {
        try {
            const headers = {
                'Authorization': `Bearer ${auth.user?.access_token}`,
                'Content-Type': 'application/json'
            }
            const requestBody: CompleteLabourRequest = {
                "end_time": new Date().toISOString(),
                "notes": labourNotes
            }
            const response = await fetch(
                'http://localhost:8000/api/v1/labour/complete',
                { method: 'PUT', headers: headers, body: JSON.stringify(requestBody) }
            );
            if (!response.ok) {
                response.text().then(text => {
                    throw new Error(JSON.parse(text)["description"])
                });
            }
            const data: LabourResponse = await response.json();
            setLabour(data.labour);
            navigate("/");
        } catch (err) {
            console.error('Error starting contraction:', err);
        }
    }
    if (completeClicked) {
        if (confirmedCompleteLabour) {
            completeLabour()
        } else {
            return <ConfirmCompleteLabourModal setConfirmedComplete={setConfirmedCompleteLabour} />
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
    return <Button size='xl' color='var(--mantine-color-pink-4)' radius="lg" variant="filled" onClick={() => setCompleteClicked(true)}>Complete Labour</Button>;
}