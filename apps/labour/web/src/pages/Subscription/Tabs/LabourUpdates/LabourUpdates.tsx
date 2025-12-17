import { useEffect, useMemo, useRef } from 'react';
import { LabourReadModel } from '@base/clients/labour_service';
import { useLabourUpdatesV2, useLabourV2Client } from '@base/hooks';
import { LabourUpdate, LabourUpdateProps } from '@labour/Tabs/Updates/LabourUpdate';
import { ImportantText } from '@shared/ImportantText/ImportantText';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { pluraliseName } from '@shared/utils';
import { ScrollArea, Space } from '@mantine/core';
import classes from '@labour/Tabs/Updates/LabourUpdates.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export function StatusUpdates({ labour }: { labour: LabourReadModel }) {
  const client = useLabourV2Client();
  const { data: labourUpdatesData } = useLabourUpdatesV2(client, labour.labour_id, 20);
  const labourUpdatesTemp = labourUpdatesData?.data || [];
  const labourUpdates = [...labourUpdatesTemp].sort((a, b) => {
    return new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
  });

  const viewport = useRef<HTMLDivElement>(null);

  const motherFirstName = labour.mother_name.split(' ')[0];

  const pluralisedBirthingPersonName = pluraliseName(motherFirstName);
  const sharedLabourBegunMessage = `Exciting news, ${motherFirstName} has started labour!`;

  const formatTime = (time: string) =>
    new Date(time).toLocaleString().slice(0, 17).replace(',', ' at');

  const renderedUpdates = useMemo(() => {
    const statusUpdateDisplay: JSX.Element[] = [];
    labourUpdates.forEach((data) => {
      let props: LabourUpdateProps | null = null;
      const baseProps = {
        id: data.labour_update_id,
        sentTime: formatTime(data.created_at),
        visibility: '',
        showMenu: false,
        showFooter: false,
      };
      if (data.labour_update_type === 'ANNOUNCEMENT') {
        if (data.application_generated) {
          props = {
            ...baseProps,
            class: classes.privateNotePanel,
            icon: '🌱',
            badgeColor: '#ff8f00',
            badgeText: 'Fern Labour',
            text: sharedLabourBegunMessage,
          };
        } else {
          props = {
            ...baseProps,
            class: classes.announcementPanel,
            icon: '📣',
            badgeColor: 'var(--mantine-primary-color-6)',
            badgeText: data.labour_update_type.split('_')[0],
            text: data.message,
          };
        }
      } else if (data.labour_update_type === 'STATUS_UPDATE') {
        props = {
          ...baseProps,
          class: classes.statusUpdatePanel,
          icon: '💫',
          badgeColor: '#24968b',
          badgeText: data.labour_update_type.split('_')[0],
          text: data.message,
        };
      }
      if (props != null) {
        statusUpdateDisplay.push(<LabourUpdate data={props} />);
      }
    });
    return statusUpdateDisplay;
  }, [labourUpdates]);

  useEffect(() => {
    if (viewport.current) {
      viewport.current.scrollTo({ top: viewport.current.scrollHeight, behavior: 'auto' });
    }
  }, [labourUpdates]);

  const completed = labour.end_time !== null;
  const activeDescription = `Curious about how things are going? ${motherFirstName} can update her status here, giving you a glimpse into her progress. Check in regularly to stay informed without needing to reach out directly.`;
  const completedDescription = `Here's where ${motherFirstName} kept everyone in the loop during her labour. These were her in-the-moment thoughts and progress notes that you checked in on.`;
  const description = completed ? completedDescription : activeDescription;
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <div className={classes.content}>
            <ResponsiveTitle title={`${pluralisedBirthingPersonName} status updates`} />
            <ResponsiveDescription description={description} marginTop={10} />
            <Space h="lg" />
            {(renderedUpdates.length > 0 && (
              <>
                <ScrollArea.Autosize mah="calc(100dvh - 390px)" viewportRef={viewport}>
                  <div className={classes.statusUpdateContainer}>{renderedUpdates}</div>
                </ScrollArea.Autosize>
                <Space h="lg" />
              </>
            )) || <ImportantText message={`${motherFirstName} hasn't posted any updates yet.`} />}
          </div>
        </div>
      </div>
    </div>
  );
}
