import { useEffect, useRef } from 'react';
import { ScrollArea, Space } from '@mantine/core';
import { LabourDTO, UserSummaryDTO } from '../../../../clients/labour_service';
import { ImportantText } from '../../../../shared-components/ImportantText/ImportantText';
import { ResponsiveDescription } from '../../../../shared-components/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '../../../../shared-components/ResponsiveTitle/ResponsiveTitle';
import { pluraliseName } from '../../../../shared-components/utils';
import { LabourUpdate, LabourUpdateProps } from '../../../Labour/Tabs/Updates/LabourUpdate';
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
  const pluralisedBirthingPersonName = pluraliseName(birthingPerson.first_name);
  const sharedLabourBegunMessage = `Exciting news, ${birthingPerson.first_name} has started labour!`;

  const statusUpdateDisplay = labourUpdates.map((data) => {
    let props: LabourUpdateProps;
    if (data.labour_update_type === 'announcement') {
      if (data.application_generated) {
        props = {
          id: data.id,
          sentTime: new Date(data.sent_time).toLocaleString().slice(0, 17).replace(',', ' at'),
          class: classes.privateNotePanel,
          icon: '🌱',
          badgeColor: '#ff8f00',
          badgeText: 'Fern Labour',
          text: sharedLabourBegunMessage,
          visibility: '',
          showMenu: false,
          showFooter: false,
        };
      } else {
        props = {
          id: data.id,
          sentTime: new Date(data.sent_time).toLocaleString().slice(0, 17).replace(',', ' at'),
          class: classes.announcementPanel,
          icon: '📣',
          badgeColor: 'var(--mantine-color-pink-6)',
          badgeText: data.labour_update_type.split('_')[0],
          text: data.message,
          visibility: '',
          showMenu: false,
          showFooter: false,
        };
      }
    } else {
      props = {
        id: data.id,
        sentTime: new Date(data.sent_time).toLocaleString().slice(0, 17).replace(',', ' at'),
        class: classes.statusUpdatePanel,
        icon: '💫',
        badgeColor: '#24968b',
        badgeText: data.labour_update_type.split('_')[0],
        text: data.message,
        visibility: '',
        showMenu: false,
        showFooter: false,
      };
    }
    return <LabourUpdate data={props} />;
  });

  useEffect(() => {
    if (viewport.current) {
      viewport.current.scrollTo({ top: viewport.current.scrollHeight, behavior: 'auto' });
    }
  }, [labourUpdates]);

  const completed = labour.end_time !== null;
  const activeDescription = `Curious about how things are going? ${birthingPerson.first_name} can update her status here, giving you a glimpse into her progress. Check in regularly to stay informed without needing to reach out directly.`;
  const completedDescription = `Here's where ${birthingPerson.first_name} kept everyone in the loop during her labour. These were her in-the-moment thoughts and progress notes that you checked in on.`;
  const description = completed ? completedDescription : activeDescription;
  return (
    <div className={baseClasses.root} style={{ maxHeight: 'calc(85% - 120px)' }}>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <ResponsiveTitle title={`${pluralisedBirthingPersonName} status updates`} />
            <ResponsiveDescription description={description} marginTop={10} />
            {(statusUpdateDisplay.length > 0 && (
              <ScrollArea.Autosize mt="md" mah="60svh" viewportRef={viewport}>
                <div className={classes.statusUpdateContainer}>{statusUpdateDisplay}</div>
              </ScrollArea.Autosize>
            )) || (
              <ImportantText
                message={`${birthingPerson.first_name} hasn't posted any updates yet.`}
              />
            )}
            <Space h="lg" />
          </div>
        </div>
      </div>
    </div>
  );
}
