import { useEffect, useRef, useState } from 'react';
import { ScrollArea, Stack, Textarea, Title } from '@mantine/core';
import { AnnouncementDTO } from '../../../../client';
import MakeAnnouncementButton from '../Buttons/MakeAnnouncement';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import messageClasses from './Announcements.module.css';
import classes from './LabourContainer.module.css';

export function Announcements({ announcementHistory }: { announcementHistory: AnnouncementDTO[] }) {
  const [announcement, setAnnouncement] = useState('');
  const viewport = useRef<HTMLDivElement>(null);

  const messageBubbles = announcementHistory.map((message) => (
    <div className={messageClasses.message} id={message.id}>
      <div className={messageClasses.messageLabel}>
        {new Date(message.sent_time).toLocaleString().slice(0, 17).replace(',', ' at')}
      </div>
      <div className={messageClasses.messageBubble}>{message.message}</div>
    </div>
  ));

  useEffect(() => {
    if (viewport.current) {
      viewport.current.scrollTo({ top: viewport.current.scrollHeight, behavior: 'auto' });
    }
  }, [announcementHistory]);

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.header}>
        <Title fz="xl" className={baseClasses.title}>
          Make an announcement
        </Title>
      </div>
      <div className={baseClasses.body}>
        <Stack align="stretch" justify="center">
          {announcementHistory.length > 0 && (
            <ScrollArea.Autosize mah={300} viewportRef={viewport} p={10}>
              {messageBubbles}
            </ScrollArea.Autosize>
          )}
          <Textarea
            radius="lg"
            label="Your announcement"
            description="Share an update with your subscribers."
            classNames={{
              label: classes.labourNotesLabel,
              description: classes.labourNotesDescription,
            }}
            onChange={(event) => setAnnouncement(event.currentTarget.value)}
            value={announcement}
          />
          <MakeAnnouncementButton message={announcement} setAnnouncement={setAnnouncement} />
        </Stack>
      </div>
    </div>
  );
}
