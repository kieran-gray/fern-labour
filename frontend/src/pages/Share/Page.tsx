import { useAuth } from 'react-oidc-context';
import { Header } from '../../shared-components/Header/Header';
import { ShareContainer } from './Components/Container/Container';
import { Center } from '@mantine/core';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer';
import { BirthingPersonService, OpenAPI } from '../../client';
import { useQuery } from '@tanstack/react-query';

export const ShareBirthingPersonPage = () => {
  const auth = useAuth();
  const page = 'Share';
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || ""
  }
  const userId = auth.user?.profile.sub || ""

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['token', auth.user?.profile.sub],
    queryFn: async () => {
      const response = await BirthingPersonService.getSubscriptionTokenApiV1BirthingPersonSubscriptionTokenGet()
      return response.token;
    }
  });

  if (isPending) {
    return (
        <div>
            <Header active={page}/>
            <PageLoading />
        </div>
    );
  }

  if (isError) {
    return (
      <div>
        <Header active={page}/>
        <ErrorContainer message={error.message} />
      </div>
    );
  }

  // TODO environment variable for frontend host
  const shareUrl = `https://fernlabour.com/subscribe/${userId}`
  const shareText = `Hey, follow this link and sign up to get notifications about my labour:\n\n${shareUrl}\n\nYou'll also need this code: ${data}`;

  return (
    <div>
      <Header active={page}/>
      <Center flex={"shrink"}  p={15}>
        <ShareContainer shareUrl={shareUrl} token={data} copyText={shareText}/>
      </Center>
    </div>
  );
};
