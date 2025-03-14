import { useEffect, useRef, useState } from 'react';
import { IconPencil, IconSwitchHorizontal } from '@tabler/icons-react';
import { useAuth } from 'react-oidc-context';
import { Avatar, Button, Group, Image, LoadingOverlay, ScrollArea, Text, TextInput, Title } from '@mantine/core';
import { LabourUpdateDTO } from '../../../../../client';
import { ImportantText } from '../../../../../shared-components/ImportantText/ImportantText';
import image from '../image.svg';
import { ManageStatusUpdateMenu } from './ManageStatusUpdateMenu';
import { PostStatusUpdateButton } from './PostStatusUpdate';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
import classes from './StatusUpdates.module.css';

export function StatusUpdates({
  statusUpdates,
  setActiveTab,
}: {
  statusUpdates: LabourUpdateDTO[];
  setActiveTab: Function;
}) {
  const [update, setUpdate] = useState('');
  const viewport = useRef<HTMLDivElement>(null);
  const auth = useAuth();
  const userName = auth.user?.profile.name;

  const statusUpdateDisplay = statusUpdates.map((data) => {
    return (
      <div className={classes.statusUpdatePanel} id={data.id}>
        <LoadingOverlay visible={data.id === 'placeholder'} />
        <Group>
          <Avatar alt={userName} radius="xl" color="var(--mantine-color-pink-5)" />
          <div>
            <Text size="sm" fw="700" c="var(--mantine-color-gray-9)">
              {userName}
            </Text>
            <Text size="xs" c="var(--mantine-color-gray-9)">
              {new Date(data.sent_time).toLocaleString().slice(0, 17).replace(',', ' at')}
            </Text>
          </div>
          <div style={{ flexGrow: 1 }} />
          <ManageStatusUpdateMenu statusUpdateId={data.id} />
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
              Post a status update
            </Title>
            <Title order={3} hiddenFrom="sm">
              Post a status update
            </Title>
            <Text c="var(--mantine-color-gray-7)" mt="sm" mb="md">
              Update your status here to let your subscribers know how you are getting on. They
              won't be notified about these updates, but they will be able to see them in the app.
            </Text>
            {(statusUpdateDisplay.length > 0 && (
              <ScrollArea.Autosize mah={400} viewportRef={viewport}>
                <div className={classes.statusUpdateContainer}>{statusUpdateDisplay}</div>
              </ScrollArea.Autosize>
            )) || (
              <>
                <div className={classes.imageFlexRow}>
                  <Image src={image} className={classes.image} />
                </div>
                <ImportantText message="You haven't posted any status updates yet." />
              </>
            )}
            <TextInput
              mt={20}
              rightSection={<IconPencil size={18} stroke={1.5} />}
              radius="lg"
              size="md"
              placeholder="Your status update"
              onChange={(event) => setUpdate(event.currentTarget.value)}
              value={update}
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
                onClick={() => setActiveTab('announcements')}
                type="submit"
              >
                Switch to Announcements
              </Button>
              <PostStatusUpdateButton message={update} setUpdate={setUpdate} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
