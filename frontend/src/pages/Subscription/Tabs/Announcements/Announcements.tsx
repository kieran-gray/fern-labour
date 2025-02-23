import { useEffect, useRef } from 'react';
import { ScrollArea, Text, Title } from '@mantine/core';
import { LabourDTO } from '../../../../client';
import { ContainerHeader } from '../../../../shared-components/ContainerHeader/ContainerHeader';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './Announcements.module.css';

export function Announcements({
  labour,
  birthingPersonName,
}: {
  labour: LabourDTO;
  birthingPersonName: string;
}) {
  const viewport = useRef<HTMLDivElement>(null);
  const announcements = labour.announcements;

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
      <ContainerHeader title="Announcements" />
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title order={3}>{birthingPersonName} announcements</Title>
            <Text c="var(--mantine-color-gray-7)" mt="sm" mb="md">
              Stay updated! Labour announcements will appear here, and notifications will be sent
              based on the contact methods you have set in the details tab.
            </Text>
            <ScrollArea.Autosize
              className={classes.scrollArea}
              mah={400}
              viewportRef={viewport}
              p={10}
            >
              {messageBubbles}
            </ScrollArea.Autosize>
          </div>
        </div>
      </div>
    </div>
  );
}
