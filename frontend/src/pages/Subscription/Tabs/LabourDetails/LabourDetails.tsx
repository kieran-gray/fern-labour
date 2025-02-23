import { Badge, Space, Text, Title } from '@mantine/core';
import { LabourDTO } from '../../../../client';
import { ContainerHeader } from '../../../../shared-components/ContainerHeader/ContainerHeader';
import { dueDateToGestationalAge } from '../../../../shared-components/utils';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './LabourDetails.module.css';

export default function LabourDetails({
  labour,
  birthingPersonName,
}: {
  labour: LabourDTO;
  birthingPersonName: string;
}) {
  const title = `${birthingPersonName} Labour Details`;
  return (
    <div className={baseClasses.root}>
      <ContainerHeader title={title} />
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title className={classes.title}>
              {labour.labour_name ? labour.labour_name : 'Your Labour'}
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
              <Badge variant="filled" className={classes.labourBadge} size="lg">
                {!labour.first_labour ? 'Not ' : ''}first time mother
              </Badge>
            </div>
            <Space h="xl" />
          </div>
        </div>
      </div>
    </div>
  );
}
