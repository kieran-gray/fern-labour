import { useApiAuth } from '@base/shared-components/hooks/useApiAuth';
import { SubscriptionDTO } from '@clients/labour_service';
import { useSubscriber } from '@shared/hooks';
import { ImportantText } from '@shared/ImportantText/ImportantText';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { useSearchParams } from 'react-router-dom';
import { Badge, Button, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import ContactMethodsForm from './ContactMethodsForm';
import classes from './ContactMethodsForm.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export function warnNoNumberSet(
  contactMethods: string[],
  phone_number: string | null
): string | null {
  let warning = null;
  if (
    (contactMethods.includes('sms') || contactMethods.includes('whatsapp')) &&
    phone_number === null
  ) {
    warning =
      "You have selected to receive sms or whatsapp alerts but you don't have a phone number set on your profile. Set one by clicking 'Update Profile' in the app menu.";
  }
  return warning;
}

export function warnNonUKNumber(
  contactMethods: string[],
  phone_number: string | null
): string | null {
  let warning = null;
  if (contactMethods.includes('sms') && phone_number !== null && !phone_number.startsWith('+44')) {
    warning =
      "Your mobile number isn't from the UK (it doesn't start with +44). Unfortunately we can only send SMS messages to UK numbers at this time, please select WhatsApp for international messaging.";
  }
  return warning;
}

export default function ContactMethods({ subscription }: { subscription: SubscriptionDTO }) {
  useApiAuth();
  const [searchParams] = useSearchParams();
  const [opened, { open, close }] = useDisclosure(false);
  const prompt = searchParams.get('prompt');

  const { status, data } = useSubscriber();

  let contactMethodsWarning = null;
  if (status === 'success') {
    contactMethodsWarning =
      warnNoNumberSet(subscription.contact_methods, data.user.phone_number) ||
      warnNonUKNumber(subscription.contact_methods, data.user.phone_number);
  }

  const selectedContactMethods = subscription.contact_methods.map((method) => (
    <Badge id={method} variant="filled" size="lg" color="var(--mantine-primary-color-4)">
      {method}
    </Badge>
  ));

  const description =
    "Choose how you want to hear about updates during labour. Select your preferred notification methods so you don't miss any important moments.";

  return (
    <>
      <div className={baseClasses.root}>
        <div className={baseClasses.body}>
          <div className={baseClasses.inner} style={{ paddingBottom: 0 }}>
            <div className={classes.content} style={{ marginRight: 0 }}>
              <ResponsiveTitle title="Your contact methods" />
              <ResponsiveDescription description={description} marginTop={10} />
            </div>
          </div>
          <div
            className={baseClasses.inner}
            style={{ paddingTop: 0, paddingBottom: 0, marginTop: 10 }}
          >
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
                  <Text
                    c="light-dark(var(--mantine-color-gray-7), var(--mantine-color-gray-2))"
                    mt="md"
                    mb="md"
                  >
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
                color="var(--mantine-primary-color-4)"
                variant="filled"
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
