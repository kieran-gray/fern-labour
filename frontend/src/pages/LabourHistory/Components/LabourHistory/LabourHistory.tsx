import { Image, Text, Title } from '@mantine/core';
import image from '../../../Subscriptions/Components/ManageSubscriptions/image.svg';
import { LabourHistoryTable } from './LabourHistoryTable/LabourHistoryTable';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './LabourHistory.module.css';

export function LabourHistory() {
  return (
    <div className={baseClasses.root} style={{ width: '100%', flexGrow: 1 }}>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title order={2} visibleFrom="sm">
              Your Labour History
            </Title>
            <Title order={3} hiddenFrom="sm">
              Your Labour History
            </Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              Here you can explore your complete labour history. Each entry captures the details of
              your experience, from first contraction to your baby's arrival. Select any record to
              view the full timeline and statistics.
            </Text>
            <div className={classes.imageFlexRow}>
              <Image src={image} className={classes.smallImage} />
            </div>
          </div>
          <Image src={image} className={classes.image} />
        </div>

        <div className={classes.inner} style={{ paddingTop: '0' }}>
          <LabourHistoryTable />
        </div>
      </div>
    </div>
  );
}
