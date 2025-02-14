import { Space, Text, Title, Image } from '@mantine/core';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './SubscribersContainer.module.css';
import image from './image.svg'
import { SubscribersTable } from '../SubscribersTable/SubscribersTable';

export function SubscribersContainer() {
  return (
    <>
      <div className={baseClasses.root} style={{ maxWidth: '1100px' }}>
        <div className={baseClasses.header}>
          <Title fz="xl" className={baseClasses.title}>
            Your Subscribers
          </Title>
        </div>
        <div className={baseClasses.body}>
          <div className={classes.inner}>
              <div className={classes.content}>
                <Title className={classes.title}>Manage your subscribers</Title>
                <Text c="var(--mantine-color-gray-7)" mt="md">
                  Here, you can view and manage the subscribers following your labour journey.
                  Update their roles and remove or block them if needed.
                  Stay in control of who can stay connected and support you during this special
                  time.
                </Text>
              </div>
              <div className={baseClasses.flexColumn}>
                <Image src={image} className={classes.image} />
              </div>
              </div>
              <div className={classes.inner} style={{paddingTop: '0'}}>
                <SubscribersTable />
              </div>
            </div>
          </div>
      <Space h="xl" />
    </>
  );
}
