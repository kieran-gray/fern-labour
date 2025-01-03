import { useAuth } from 'react-oidc-context';
import { useState, useEffect } from 'react';
import { Header } from '../../shared-components/Header/Header';
import { LabourDTO, LabourResponse } from '../../client';
import LabourContainer from './Components/LabourContainer/LabourContainer';
import { Center, Space } from '@mantine/core';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading';


export const LabourPage = () => {
    const [hasActiveLabour, setHasActiveLabour] = useState<boolean | null>(null);
    const [activeLabour, setActiveLabour] = useState<LabourDTO | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");
    const auth = useAuth();
    const page = 'Labour';

    useEffect(() => {
        const fetchActiveLabour = async () => {
            try {
                const headers = {
                    'Authorization': `Bearer ${auth.user?.access_token}`
                }
                const response = await fetch('http://localhost:8000/api/v1/labour/active', { method: 'GET', headers: headers });
                if (!response.ok) {
                    if (response.status == 404) {
                        setHasActiveLabour(false);
                        setIsLoading(false);
                    } else {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                }
                const data: LabourResponse = await response.json();
                setHasActiveLabour(true);
                setActiveLabour(data.labour);
                setIsLoading(false);
            } catch (err) {
                console.error('Error fetching labour data:', err);
                setError('Failed to load labour. Please try again later.');
                setIsLoading(false);
            }
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
            <div>
            <Header active={page}/>
            <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
                <div className="text-xl text-red-600">{error}</div>
            </div>
            </div>
        );
    }
    const bannerProps = {
        labour: activeLabour,
        hasActiveLabour: hasActiveLabour,
        setLabour: setActiveLabour,
        }
    return (
        <div>
        <Header active={page}/>
        <Center flex={"shrink"} p={15}>
            <LabourContainer {...bannerProps} />
        </Center>
        <Space h="xl"></Space>
        </div>
    )
};
