import { useEffect, useRef, useState } from 'react';
import { IconPencil, IconSwitchHorizontal } from '@tabler/icons-react';
import { Button, ScrollArea, Text, TextInput, Title } from '@mantine/core';
import { LabourUpdateDTO } from '../../../../../client';
import MakeAnnouncementButton from './MakeAnnouncement';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
import classes from './Announcements.module.css';

export function Announcements({
  announcements,
  setActiveTab,
}: {
  announcements: LabourUpdateDTO[];
  setActiveTab: Function;
}) {
  const [announcement, setAnnouncement] = useState('');
  const viewport = useRef<HTMLDivElement>(null);

  const messageBubbles = announcements.map((message) => (
    <div className={classes.message} id={message.id}>
      <div className={classes.messageLabel}>
        {new Date(message.sent_time).toLocaleString().slice(0, 17).replace(',', ' at')}
      </div>
      <div className={classes.messageBubble}>{message.message}</div>
    </div>
  ));

  useEffect(() => {
    if (viewport.current) {
      viewport.current.scrollTo({ top: viewport.current.scrollHeight, behavior: 'auto' });
    }
  }, [announcements]);

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title order={3}>Make an announcement</Title>
            <Text c="var(--mantine-color-gray-7)" mt="sm" mb="md">
              Make an announcement to all your subscribers—they’ll be notified through their
              preferred methods. Use this to share important updates.
            </Text>
            <ScrollArea.Autosize mah={400} viewportRef={viewport} p={10}>
              {messageBubbles}
            </ScrollArea.Autosize>
            <TextInput
              rightSection={<IconPencil size={18} stroke={1.5} />}
              radius="lg"
              size="md"
              placeholder="Your announcement"
              onChange={(event) => setAnnouncement(event.currentTarget.value)}
              value={announcement}
            />
            <div className={classes.flexRow} style={{ marginTop: '10px' }}>
              <Button
                color="var(--mantine-color-pink-4)"
                leftSection={<IconSwitchHorizontal size={18} stroke={1.5} />}
                variant="outline"
                radius="xl"
                size="md"
                h={48}
                className={classes.backButton}
                onClick={() => setActiveTab('statusUpdates')}
                type="submit"
              >
                Switch to Status Updates
              </Button>
              <MakeAnnouncementButton message={announcement} setAnnouncement={setAnnouncement} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
