import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Badge, Text } from '@mantine/core';
import { ApiError, OpenAPI, SubscriberService } from '../../../client';
import { NotFoundError } from '../../../Errors';
import ContactMethodsModal from '../../../shared-components/ContactMethodsModal/ContactMethodsModal';
import { LabourSummaryStatistics } from '../../../shared-components/LabourStatistics/LabourSummaryStatistics';
import { ContainerLoadingIcon } from '../../../shared-components/PageLoading/Loading';
import baseClasses from '../../../shared-components/shared-styles.module.css';

export default function Subscriptions() {
  const auth = useAuth();
  const [askContactMethods, setAskContactMethods] = useState(false);

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['subscriptions', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await SubscriberService.getSubscriptionsApiV1SubscriberSubscriptionsGet();
        return response.subscriptions;
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) {
          setAskContactMethods(true);
          throw new NotFoundError();
        }
        throw new Error('Failed to load subscriptions. Please try again later.');
      }
    },
    placeholderData: [],
    retry: (failureCount, error) => {
      if (error instanceof NotFoundError) {
        return false;
      }
      return failureCount < 3;
    },
  });

  if (isPending) {
    return (
      <div className={baseClasses.body}>
        <Text className={baseClasses.text}>
          <ContainerLoadingIcon />
        </Text>
      </div>
    );
  }

  if (isError) {
    if (askContactMethods) {
      return <ContactMethodsModal promptForContactMethods={setAskContactMethods} />;
    } else if (!data) {
      return (
        <div className={baseClasses.body}>
          <Text className={baseClasses.text}>Error: {error.message}</Text>
        </div>
      );
    }
  }

  const subscriptionsElements = data.map((subscription) => (
    <div key={subscription.id} className={baseClasses.body}>
      <div className={baseClasses.flexRowNoBP}>
        <Text className={baseClasses.text}>
          {subscription.first_name} {subscription.last_name}
        </Text>
        <Badge size="lg" mb={20} pl={40} pr={40} variant="light">
          {subscription.active_labour ? 'In Labour' : 'Not In Labour'}
        </Badge>
      </div>
      {subscription.active_labour && (
        <LabourSummaryStatistics labour={subscription.active_labour} inContainer={false} />
      )}
    </div>
  ));
  return (
    <>
      {subscriptionsElements}
      {data.length === 0 && (
        <div className={baseClasses.body}>
          <div className={baseClasses.text}>
            Subscribe to someone to see their labour details here
          </div>
        </div>
      )}
    </>
  );
}
