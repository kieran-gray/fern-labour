import classes from './LabourContainer.module.css'
import baseClasses from '../../../../shared-components/shared-styles.module.css'
import { useState } from 'react';
import { Stack, Textarea, Title } from '@mantine/core';
import MakeAnnouncementButton from '../Buttons/MakeAnnouncement';


export function Announcements() {
  const [announcement, setAnnouncement] = useState("");
  return (
    <div className={baseClasses.root}>
    <div className={baseClasses.header}>
      <Title fz="xl" className={baseClasses.title}>Make an announcement</Title>
    </div>
    <div className={baseClasses.body}>
      <Stack align='stretch' justify='center' gap='md'>
        <Textarea
            radius="lg"
            label="Your announcement"
            description="Share an update with your subscribers."
            classNames={
                { 
                    label: classes.labourNotesLabel,
                    description: classes.labourNotesDescription
                }
            }
            onChange={(event) => setAnnouncement(event.currentTarget.value)}
            value={announcement}
        />
        <MakeAnnouncementButton message={announcement} setAnnouncement={setAnnouncement} />
      </Stack>
    </div>
    </div>
  )
}

