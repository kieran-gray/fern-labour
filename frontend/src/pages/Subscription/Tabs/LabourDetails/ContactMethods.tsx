import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useSearchParams } from 'react-router-dom';
import { Badge, Button, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { SubscriptionDTO, UserService } from '../../../../client';
import { ImportantText } from '../../../../shared-components/ImportantText/ImportantText';
import { ResponsiveTitle } from '../../../../shared-components/ResponsiveTitle/ResponsiveTitle';
import ContactMethodsForm from './ContactMethodsForm';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './ContactMethodsForm.module.css';

export default function ContactMethods({ subscription }: { subscription: SubscriptionDTO }) {
  const auth = useAuth();
  const [searchParams] = useSearchParams();
  const [opened, { open, close }] = useDisclosure(false);
  const prompt = searchParams.get('prompt');

  const { status, data } = useQuery({
    queryKey: ['subscriber', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await UserService.getUser();
        return response;
      } catch (err) {
        throw new Error('Failed to load subscriber. Please try again later.');
      }
    },
  });

  let contactMethodsWarning = null;
  if (status === 'success') {
    if (subscription.contact_methods.includes('sms')) {
      if (data.user.phone_number == null) {
        contactMethodsWarning =
          "You have selected to receive text message alerts but you don't have a phone number set on your profile. Set one by clicking 'Update Profile' in the app menu.";
      } else if (!data.user.phone_number?.startsWith('+44')) {
        contactMethodsWarning =
          "Your mobile number isn't from the UK (it doesn't start with +44). Unfortunately we can only send text messages to UK numbers at this time.";
      }
    }
  }

  const selectedContactMethods = subscription.contact_methods.map((method) => (
    <Badge id={method} variant="filled" size="lg" color="var(--mantine-color-pink-4)">
      {method}
    </Badge>
  ));

  return (
    <>
      <div className={baseClasses.root}>
        <div className={baseClasses.body}>
          <div className={baseClasses.inner} style={{ paddingBottom: 0 }}>
            <div className={classes.content} style={{ marginRight: 0 }}>
              <ResponsiveTitle title="Your contact methods" />
              <Text c="var(--mantine-color-gray-7)" mt="md" mb="md">
                Choose how you want to hear about updates during labour. Select your preferred
                notification methods so you don't miss any important moments.
              </Text>
            </div>
          </div>
          <div className={baseClasses.inner} style={{ paddingTop: 0, paddingBottom: 0 }}>
            <div className={baseClasses.content}>
              {subscription.contact_methods.length === 0 && (
                <div style={{ marginTop: '10px' }}>
                  <ImportantText message=" You will only receive live notifications if you add your preferred methods below" />
                </div>
              )}
              {contactMethodsWarning != null && (
                <div style={{ marginBottom: '20px' }}>
                  <ImportantText message={contactMethodsWarning} />
                </div>
              )}
              {subscription.contact_methods.length > 0 && (
                <>
                  <Text c="var(--mantine-color-gray-7)" mt="md" mb="md">
                    Your chosen contact methods:
                  </Text>
                  <div className={classes.infoRow}>{selectedContactMethods}</div>
                </>
              )}
            </div>
          </div>
          <div className={baseClasses.inner} style={{ paddingTop: 0 }}>
            <div className={classes.submitRow}>
              <Button
                color="var(--mantine-color-pink-4)"
                variant="outline"
                radius="xl"
                size="md"
                h={48}
                onClick={() => open()}
                className={classes.submitButton}
                styles={{ section: { marginRight: 22 } }}
                type="submit"
              >
                Update Contact Methods
              </Button>
            </div>
          </div>
        </div>
      </div>
      <ContactMethodsForm
        subscription={subscription}
        opened={opened || prompt === 'contactMethods'}
        close={close}
      />
    </>
  );
}
