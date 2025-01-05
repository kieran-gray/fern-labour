import { useAuth } from 'react-oidc-context';
import { useState, useEffect } from 'react';
import { Header } from '../../shared-components/Header/Header';
import { ApiError, LabourDTO, LabourService, OpenAPI } from '../../client';
import LabourContainer from './Components/LabourContainer/LabourContainer';
import { Center, Space } from '@mantine/core';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer';


export const LabourPage = () => {
    const [hasActiveLabour, setHasActiveLabour] = useState<boolean | null>(null);
    const [activeLabour, setActiveLabour] = useState<LabourDTO | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");
    const auth = useAuth();
    const page = 'Labour';
    OpenAPI.TOKEN = async () => {
        return auth.user?.access_token || ""
    }

    useEffect(() => {
        const fetchActiveLabour = async () => {
            let activeLabour
            try {
                const response = await LabourService.getActiveLabourApiV1LabourActiveGet()
                activeLabour = response.labour
            } catch (err) {
                if (err instanceof ApiError) {
                    if (err.status !== 404) {
                        setError("Failed to load labour. Please try again later.")
                    }
                } else {
                    setError("Failed to load labour. Please try again later.")
                }
            }
            if (activeLabour) {
                setActiveLabour(activeLabour);
            }
            // TODO this logic makes no sense BUT if there is an error then that will be displayed
            //      if there is no error then there should be an active labour. Without this, the 
            //      labour container doesn't update to show the new labour for some reason.
            setHasActiveLabour(true);
            setIsLoading(false);
        }
        if (activeLabour === null) {
            fetchActiveLabour();
        }
    }, []);

    if (isLoading) {
        return (
            <div>
                <Header active={page}/>
                <PageLoading />
            </div>
        );
    }

    if (error) {
        return (
        <>
            <Header active={page}/>
            <ErrorContainer message={error} />
        </>);
    }

    return (
        <>
        <Header active={page}/>
        <Center flex={"shrink"} p={15}>
            <LabourContainer labour={activeLabour} hasActiveLabour={hasActiveLabour} setLabour={setActiveLabour} />
        </Center>
        <Space h="xl"></Space>
        </>
    )
};
