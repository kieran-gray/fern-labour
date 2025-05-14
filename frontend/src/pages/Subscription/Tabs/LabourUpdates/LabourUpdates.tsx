import { useEffect, useRef } from 'react';
import { ScrollArea, Text } from '@mantine/core';
import { LabourDTO, UserSummaryDTO } from '../../../../clients/labour_service';
import { ImportantText } from '../../../../shared-components/ImportantText/ImportantText';
import { ResponsiveTitle } from '../../../../shared-components/ResponsiveTitle/ResponsiveTitle';
import { pluraliseName } from '../../../../shared-components/utils';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from '../../../Labour/Tabs/Updates/LabourUpdates.module.css';
import { LabourUpdate } from '../../../Labour/Tabs/Updates/LabourUpdate';

export function StatusUpdates({
  labour,
  birthingPerson,
}: {
  labour: LabourDTO;
  birthingPerson: UserSummaryDTO;
}) {
  const labourUpdates = labour.labour_updates;
  const viewport = useRef<HTMLDivElement>(null);
  const pluralisedBirthingPersonName = pluraliseName(birthingPerson.first_name);

  const statusUpdateDisplay = labourUpdates.map((data) => {
    return <LabourUpdate data={data} completed={false} owner={false} />;
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
    <div className={baseClasses.root} style={{maxHeight: "calc(85% - 120px)"}}>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <ResponsiveTitle title={`${pluralisedBirthingPersonName} status updates`} />
            <Text c="var(--mantine-color-gray-7)" mt="sm" mb="md">
              {completed ? completedDescription : activeDescription}
            </Text>
            {(statusUpdateDisplay.length > 0 && (
              <ScrollArea.Autosize mah="60svh" viewportRef={viewport}>
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
