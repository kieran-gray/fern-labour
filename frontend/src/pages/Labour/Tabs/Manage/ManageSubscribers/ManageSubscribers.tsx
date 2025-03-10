import { Image, Text, Title } from '@mantine/core';
import image from '../../../../Subscribe/Components/protected.svg';
import { SubscribersTable } from './SubscribersTable/SubscribersTable';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
import classes from './ManageSubscribers.module.css';

export function SubscribersContainer() {
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title order={3}>Manage your subscribers</Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              Here, you can view and manage the subscribers following your labour journey. Update
              their roles and remove or block them if needed. Stay in control of who can stay
              connected and support you during this special time.
            </Text>
          </div>
          <div className={baseClasses.flexColumn}>
            <Image src={image} className={classes.image} />
          </div>
        </div>
        <div className={classes.inner} style={{ paddingTop: '0' }}>
          <SubscribersTable />
        </div>
      </div>
    </div>
  );
}
