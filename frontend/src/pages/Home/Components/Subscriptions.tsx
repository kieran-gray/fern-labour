import { Badge, Text } from '@mantine/core';
import baseClasses from '../../../shared-components/shared-styles.module.css';
import { ApiError, OpenAPI, SubscriberService } from '../../../client';
import { useAuth } from 'react-oidc-context';
import { useQuery } from '@tanstack/react-query';
import ContactMethodsModal from '../../../shared-components/ContactMethodsModal/ContactMethodsModal';
import { NotFoundError } from '../../../Errors';
import { useState } from 'react';
import { ContainerLoadingIcon } from '../../../shared-components/PageLoading/Loading';


const formatLabourDurationHours = (hours: number): string => {
  const wholeHours = Math.round(hours);
  if (wholeHours < 1) {
    return "Less than 1 hour"
  } else if (wholeHours == 1) {
    return `${wholeHours} hour`
  } else {
    return `${wholeHours} hours`
  }
}

export default function Subscriptions() {
  const auth = useAuth();
  const [askContactMethods, setAskContactMethods] = useState(false)

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || ""
  }

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
            throw new Error("Failed to load subscriptions. Please try again later.")
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
        <Text className={baseClasses.text}><ContainerLoadingIcon /></Text>
      </div>
    )
  }

  if (isError) {
    if (askContactMethods) {
      return <ContactMethodsModal promptForContactMethods={setAskContactMethods} />
    } else if (!data) {
      return (
        <div className={baseClasses.body}>
          <Text className={baseClasses.text}>Error: {error.message}</Text>
        </div>
      )
    }
  }

  const subscriptionsElements = data.map((subscription) => (
    <div key={subscription.id} className={baseClasses.body}>
      <div className={baseClasses.flexRowNoBP}>
        <Text className={baseClasses.text}>{subscription.first_name} {subscription.last_name}</Text>
        <Badge size='lg' mb={20} pl={40} pr={40} variant="light">{subscription.active_labour ? 'In Labour' : 'Not In Labour'}</Badge>
      </div>
      {subscription.active_labour && 
        <>
          <Text className={baseClasses.text}>Number of contractions: {subscription.active_labour.contraction_count}</Text>
          <Text className={baseClasses.text}></Text>
          <Text className={baseClasses.text}>Labour duration: {formatLabourDurationHours(subscription.active_labour.duration)}</Text>
          <Text className={baseClasses.text}>Current phase: {subscription.active_labour.current_phase}</Text>
          <Text className={baseClasses.text}>Hospital recommended: {String(subscription.active_labour.hospital_recommended)}</Text>
        </>
      }
    </div>
  ));
  return (
    <>
      {subscriptionsElements}
      {data.length == 0 && 
        <div className={baseClasses.body}>
          <div className={baseClasses.text}>Subscribe to someone to see their labour details here</div>
        </div>
      }
    </>
  )
}
