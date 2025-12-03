import { useSubscription } from '@base/contexts/SubscriptionContext';
import { useApiAuth, useCreateCheckoutSession } from '@shared/hooks';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { IconArrowUp } from '@tabler/icons-react';
import { Button, Image, Text } from '@mantine/core';
import image from './ShareMore.svg';
import classes from './PayWall.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export const PayWall = () => {
  useApiAuth();
  const { subscriptionId } = useSubscription();
  const createCheckout = useCreateCheckoutSession();

  const handleUpgrade = () => {
    const baseUrl = window.location.href.split('?')[0];
    const returnURL = new URL(baseUrl);

    const successUrl = new URL(returnURL);
    successUrl.searchParams.set('prompt', 'contactMethods');

    const cancelUrl = new URL(returnURL);
    cancelUrl.searchParams.set('cancelled', 'true');

    createCheckout.mutate({
      subscriptionId: subscriptionId!,
      successUrl: successUrl.toString(),
      cancelUrl: cancelUrl.toString(),
    });
  };
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
              disabled={createCheckout.isPending}
              onClick={handleUpgrade}
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
