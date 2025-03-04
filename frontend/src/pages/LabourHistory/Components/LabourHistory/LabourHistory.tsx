import { Text, Title } from '@mantine/core';
import { ContainerHeader } from '../../../../shared-components/ContainerHeader/ContainerHeader';
import { LabourHistoryTable } from './LabourHistoryTable/LabourHistoryTable';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './LabourHistory.module.css';

export function LabourHistory() {
  return (
    <div className={baseClasses.root} style={{ width: '100%' }}>
      <ContainerHeader title="Your Labour History" />
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title order={3}>Your past and present labours</Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              Here, you can view all of your past and present labours. Soon you will be able to
              revisit a labour after you have completed it.
            </Text>
          </div>
        </div>
        <div className={classes.inner} style={{ paddingTop: '0' }}>
          <LabourHistoryTable />
        </div>
      </div>
    </div>
  );
}
