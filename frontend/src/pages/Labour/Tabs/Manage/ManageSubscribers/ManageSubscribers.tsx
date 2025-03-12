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
            <Title order={3} hiddenFrom="sm">
              Manage your subscribers
            </Title>
            <Title order={2} visibleFrom="sm">
              Manage your subscribers
            </Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              Here, you can view and manage your subscribers. Stay in control of who can view your
              labour by removing or blocking unwanted subscribers.
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
