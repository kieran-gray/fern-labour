import { useEffect, useRef } from 'react';
import { Avatar, Group, ScrollArea, Text } from '@mantine/core';
import { LabourDTO, UserSummaryDTO } from '../../../../client';
import { ImportantText } from '../../../../shared-components/ImportantText/ImportantText';
import { ResponsiveTitle } from '../../../../shared-components/ResponsiveTitle/ResponsiveTitle';
import { pluraliseName } from '../../../../shared-components/utils';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from '../../../Labour/Tabs/Updates/LabourUpdates.module.css';

export function StatusUpdates({
  labour,
  birthingPerson,
}: {
  labour: LabourDTO;
  birthingPerson: UserSummaryDTO;
}) {
  const labourUpdates = labour.labour_updates;
  const viewport = useRef<HTMLDivElement>(null);
  const birthingPersonName = `${birthingPerson.first_name} ${birthingPerson.last_name}`;
  const pluralisedBirthingPersonName = pluraliseName(birthingPerson.first_name);

  const statusUpdateDisplay = labourUpdates.map((data) => {
    return (
      <div className={classes.statusUpdatePanel} id={data.id}>
        <Group>
          <Avatar alt={birthingPersonName} radius="xl" color="var(--mantine-color-pink-5)" />
          <div>
            <Text size="sm" fw="700" c="var(--mantine-color-gray-9)">
              {birthingPersonName}
            </Text>
            <Text size="xs" c="var(--mantine-color-gray-9)">
              {new Date(data.sent_time).toLocaleString().slice(0, 17).replace(',', ' at')}
            </Text>
          </div>
        </Group>
        <Text pl={54} pt="sm" size="sm" fw="400">
          {data.message}
        </Text>
      </div>
    );
  });

  useEffect(() => {
    if (viewport.current) {
      viewport.current.scrollTo({ top: viewport.current.scrollHeight, behavior: 'auto' });
    }
  }, [labourUpdates]);

  const completed = labour.end_time !== null;
  const activeDescription = `Curious about how things are going? ${birthingPerson.first_name} can update her status here, giving you a glimpse into her progress. Check in regularly to stay informed without needing to reach out directly.`;
  const completedDescription = `Here's where ${birthingPerson.first_name} kept everyone in the loop during her labour. These were her in-the-moment thoughts and progress notes that you checked in on.`;

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <ResponsiveTitle title={`${pluralisedBirthingPersonName} status updates`} />
            <Text c="var(--mantine-color-gray-7)" mt="sm" mb="md">
              {completed ? completedDescription : activeDescription}
            </Text>
            {(statusUpdateDisplay.length > 0 && (
              <ScrollArea.Autosize mah={500} viewportRef={viewport}>
                <div className={classes.statusUpdateContainer}>{statusUpdateDisplay}</div>
              </ScrollArea.Autosize>
            )) || (
              <ImportantText
                message={`${birthingPerson.first_name} hasn't posted any updates yet.`}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
