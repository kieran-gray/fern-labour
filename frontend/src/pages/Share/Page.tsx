import { useAuth } from 'react-oidc-context';
import { useState, useEffect } from 'react';
import { Header } from '../../shared-components/Header/Header';
import { ShareContainer } from './Components/Container/Container';
import { Center } from '@mantine/core';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer';
import { BirthingPersonService, OpenAPI } from '../../client';

export const ShareBirthingPersonPage = () => {
  const [token, setToken] = useState('');
  const [userId, setUserId] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const auth = useAuth();
  const page = 'Share';
  OpenAPI.TOKEN = async () => {
          return auth.user?.access_token || ""
  }

  useEffect(() => {
    const fetchToken = async () => {
      try {
        const response = await BirthingPersonService.getSubscriptionTokenApiV1BirthingPersonSubscriptionTokenGet()
        setToken(response.token);
        setIsLoading(false);
        setUserId(auth.user?.profile.sub || "");
      } catch (err) {
        setError("Failed to load the sharing code. Please try again later.");
        setIsLoading(false);
      }
    };
    fetchToken();
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
        <ErrorContainer message={error} />
      </div>
    );
  }

  const shareText = `Hey, follow this link and sign up to get notifications about my labour:\n\nhttps://fernlabour.com/subscribe/${userId}\n\nYou'll also need this code: ${token}`;

  return (
    <div>
      <Header active={page}/>
      <Center flex={"shrink"}  p={15}>
        <ShareContainer userId={userId} token={token} copyText={shareText}/>
      </Center>
    </div>
  );
};
