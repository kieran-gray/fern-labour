import { Badge, Space, Text, Title } from '@mantine/core';
import { LabourDTO, SubscriptionDTO } from '../../../../client';
import { dueDateToGestationalAge } from '../../../../shared-components/utils';
import ContactMethodsForm from './ContactMethodsForm';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from '../../../Labour/Tabs/Manage/LabourDetails/LabourDetails.module.css';

export default function LabourDetails({
  labour,
  birthingPersonName,
  subscription,
}: {
  labour: LabourDTO;
  birthingPersonName: string;
  subscription: SubscriptionDTO;
}) {
  const title = labour.labour_name ? labour.labour_name : `${birthingPersonName} Labour`;
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner} style={{ paddingBottom: 0 }}>
          <div className={classes.content} style={{ marginRight: 0 }}>
            <Title order={1} visibleFrom="sm">
              {title}
            </Title>
            <Title order={2} hiddenFrom="sm">
              {title}
            </Title>
            <Text c="var(--mantine-color-gray-7)" mt="md" mb="md">
              You’re here to support someone on an incredible journey, and that means giving them
              the space they need during labour. Instead of reaching out directly, check the app for
              updates or turn on notifications below to stay informed. Your encouragement means the
              world—thank you for being part of this special moment!
            </Text>
            <div className={classes.infoRow}>
              <Badge variant="filled" className={classes.labourBadge} size="lg">
                {labour.current_phase === 'planned'
                  ? 'Not in labour'
                  : `In ${labour.current_phase} labour`}
              </Badge>
              <Badge variant="filled" className={classes.labourBadge} size="lg">
                Due: {new Date(labour.due_date).toLocaleDateString()}
              </Badge>
              <Badge variant="filled" className={classes.labourBadge} size="lg">
                Gestational age: {dueDateToGestationalAge(new Date(labour.due_date))}
              </Badge>
            </div>
          </div>
        </div>
        <Space h="xl" />
        <div className={baseClasses.inner} style={{ paddingTop: 0 }}>
          <ContactMethodsForm subscription={subscription} />
        </div>
      </div>
    </div>
  );
}
