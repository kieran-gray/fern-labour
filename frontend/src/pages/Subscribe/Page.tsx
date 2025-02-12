import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useParams, useSearchParams } from 'react-router-dom';
import { Center } from '@mantine/core';
import { ApiError, OpenAPI, SubscriberService } from '../../client';
import { NotFoundError } from '../../Errors';
import ContactMethodsModal from '../../shared-components/ContactMethodsModal/ContactMethodsModal';
import { Header } from '../../shared-components/Header/Header';
import SubscribeForm from './Components/Form';

export const SubscribePage: React.FC = () => {
  const [newUser, setNewUser] = useState<boolean>(false);
  const auth = useAuth();
  const { id } = useParams<'id'>();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  if (!id) {
    throw new Error('id is required');
  }
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  useQuery({
    queryKey: ['subscriber', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await SubscriberService.getApiV1SubscriberGet();
        return response.subscriber;
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) {
          setNewUser(true);
          throw new NotFoundError();
        }
        throw new Error('Failed to load subscriber. Please try again later.');
      }
    },
    retry: (failureCount, error) => {
      if (error instanceof NotFoundError) {
        setNewUser(true);
        return false;
      }
      return failureCount < 3;
    },
  });

  if (newUser) {
    return <ContactMethodsModal promptForContactMethods={setNewUser} />;
  }
  return (
    <div>
      <Header active="" />
      <Center flex="shrink"  p={15}>
        <SubscribeForm birthingPersonId={id} token={token} />
      </Center>
    </div>
  );
};
