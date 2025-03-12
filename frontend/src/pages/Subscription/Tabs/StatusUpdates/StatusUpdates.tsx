import { useEffect, useRef } from 'react';
import { Avatar, Group, ScrollArea, Text, Title } from '@mantine/core';
import { LabourDTO, UserSummaryDTO } from '../../../../client';
import { ImportantText } from '../../../../shared-components/ImportantText/ImportantText';
import { pluraliseName } from '../../../../shared-components/utils';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from '../../../Labour/Tabs/Updates/StatusUpdates/StatusUpdates.module.css';

export function StatusUpdates({
  labour,
  birthingPerson,
}: {
  labour: LabourDTO;
  birthingPerson: UserSummaryDTO;
}) {
  const statusUpdates = labour.status_updates;
  const viewport = useRef<HTMLDivElement>(null);
  const birthingPersonName = `${birthingPerson.first_name} ${birthingPerson.last_name}`;
  const pluralisedBirthingPersonName = pluraliseName(birthingPerson.first_name);

  const statusUpdateDisplay = statusUpdates.map((data) => {
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
  }, [statusUpdates]);

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title order={2} visibleFrom="sm">
              {pluralisedBirthingPersonName} status updates
            </Title>
            <Title order={3} hiddenFrom="sm">
              {pluralisedBirthingPersonName} status updates
            </Title>
            <Text c="var(--mantine-color-gray-7)" mt="sm" mb="md">
              Curious about how things are going? {birthingPerson.first_name} can update her status
              here, giving you a glimpse into her progress. These updates won’t send alerts, so
              check in regularly to stay informed without needing to reach out directly.
            </Text>
            {(statusUpdateDisplay.length > 0 && (
              <ScrollArea.Autosize mah={500} viewportRef={viewport}>
                <div className={classes.statusUpdateContainer}>{statusUpdateDisplay}</div>
              </ScrollArea.Autosize>
            )) || (
              <ImportantText
                message={`${birthingPerson.first_name} hasn't posted any status updates yet.`}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
