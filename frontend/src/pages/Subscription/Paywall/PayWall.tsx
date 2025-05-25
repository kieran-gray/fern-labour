import { useState } from 'react';
import { ApiError, CreateCheckoutRequest, OpenAPI, PaymentsService } from '@clients/labour_service';
import { Error } from '@shared/Notifications';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { IconArrowUp } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button, Image, Text } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { useSubscription } from '../SubscriptionContext';
import image from './ShareMore.svg';
import classes from './PayWall.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export const PayWall = () => {
  const auth = useAuth();
  const { subscriptionId } = useSubscription();
  const [mutationInProgress, setMutationInProgress] = useState<boolean>(false);

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const queryClient = useQueryClient();

  const stripeCheckout = useMutation({
    mutationFn: async () => {
      setMutationInProgress(true);
      const baseUrl = window.location.href.split('?')[0];
      const returnURL = new URL(baseUrl);

      const successUrl = new URL(returnURL);
      successUrl.searchParams.set('prompt', 'contactMethods');

      const cancelUrl = new URL(returnURL);
      cancelUrl.searchParams.set('cancelled', 'true');

      const requestBody: CreateCheckoutRequest = {
        upgrade: 'supporter',
        subscription_id: subscriptionId!,
        success_url: successUrl.toString(),
        cancel_url: cancelUrl.toString(),
      };
      return await PaymentsService.createCheckoutSession({ requestBody });
    },
    onSuccess: async (data) => {
      window.location.href = data.url!;
      queryClient.invalidateQueries({ queryKey: ['labour', auth.user?.profile.sub] });
      setMutationInProgress(false);
    },
    onError: async (error) => {
      let message = 'Unknown error occurred';
      if (error instanceof ApiError) {
        try {
          const body = error.body as { description: string };
          message = body.description;
        } catch {
          // Do nothing
        }
      }
      setMutationInProgress(false);
      notifications.show({
        ...Error,
        title: 'Error',
        message,
      });
    },
    onSettled: () => {
      setMutationInProgress(false);
    },
  });
  const title = 'Want live notifications?';
  const description = (
    <>
      Upgrade your subscription now to get live notifications to your phone.
      <br />
      Choose between SMS*, WhatsApp, and Email notifications so you never miss an update.
    </>
  );

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <div className={baseClasses.flexColumn}>
            <ResponsiveTitle title={title} />
            <ResponsiveDescription description={description} marginTop={10} />
            <div className={classes.imageFlexRow} style={{ marginTop: '20px' }}>
              <Image src={image} className={classes.smallImage} />
            </div>
            <Button
              leftSection={<IconArrowUp size={18} stroke={1.5} />}
              variant="filled"
              radius="xl"
              size="lg"
              disabled={mutationInProgress}
              onClick={() => stripeCheckout.mutate()}
            >
              Upgrade now
            </Button>
            <Text mt={15} size="xs" className={baseClasses.description}>
              *SMS messages are only supported for UK (+44) phone numbers{' '}
            </Text>
          </div>
          <Image src={image} className={classes.image} />
        </div>
      </div>
    </div>
  );
};
