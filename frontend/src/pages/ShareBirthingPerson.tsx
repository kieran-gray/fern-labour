import { useAuth } from 'react-oidc-context';
import { useState, useEffect } from 'react';
import { Header } from '../components/Header/Header';
import { ShareBanner } from '../components/ShareBanner/ShareBanner';
import { Container } from '@mantine/core';
import { PageLoading } from '../components/PageLoading/PageLoading';

export const ShareBirthingPersonPage = () => {
  const [token, setToken] = useState('');
  const [userId, setUserId] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  const auth = useAuth();
  const page = 'Share';

  useEffect(() => {
    const fetchToken = async () => {
      try {
        const headers = {
          'Authorization': `Bearer ${auth.user?.access_token}`
        }
        const response = await fetch(
          'http://localhost:8000/api/v1/birthing-person/subscription-token', { method: 'GET', headers: headers }
        );
        if (!response.ok) {
          throw new Error('Failed to fetch token');
        }
        const data = await response.json();
        setToken(data.token);
        setIsLoading(false);
        if (auth.user) {
          setUserId(auth.user.profile.sub);
        }
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
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-xl text-red-600">{error}</div>
        </div>
      </div>
    );
  }

  const shareText = `Hey, follow this link and sign up to get notifications about my labour:\n\nhttps://fernlabour.com/subscribe/${userId}\n\nYou'll also need this code: ${token}`;

  const bannerProps = {
    userId: userId,
    token: token,
    copyText: shareText
  }
  return (
    <div>
      <Header active={page}/>
      <Container size={900} p={0}>
        <ShareBanner {...bannerProps}/>
      </Container>
    </div>
  );
};
