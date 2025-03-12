import { Image, Text, Title } from '@mantine/core';
import image from './image.svg';
import { SubscriptionsTable } from './SubscriptionsTable/SubscriptionsTable';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './ManageSubscriptions.module.css';

export function SubscriptionsContainer() {
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title order={2} visibleFrom="sm">
              Manage your subscriptions
            </Title>
            <Title order={3} hiddenFrom="sm">
              Manage your subscriptions
            </Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              Here, you can view and manage the labours that you are subscribed to. Update your
              contact methods for each individually.
            </Text>
          </div>
          <div className={baseClasses.flexColumn}>
            <Image src={image} className={classes.image} />
          </div>
        </div>
        <div className={classes.inner} style={{ paddingTop: '0' }}>
          <SubscriptionsTable />
        </div>
      </div>
    </div>
  );
}
