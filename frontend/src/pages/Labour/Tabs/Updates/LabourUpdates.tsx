import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { IconPencil } from '@tabler/icons-react';
import { useAuth } from 'react-oidc-context';
import { Image, ScrollArea, Text, TextInput } from '@mantine/core';
import { LabourDTO } from '../../../../clients/labour_service';
import { ImportantText } from '../../../../shared-components/ImportantText/ImportantText';
import { ResponsiveTitle } from '../../../../shared-components/ResponsiveTitle/ResponsiveTitle';
import image from './image.svg';
import { LabourUpdate } from './LabourUpdate';
import MakeAnnouncementButton from './MakeAnnouncement';
import { PostStatusUpdateButton } from './PostStatusUpdate';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './LabourUpdates.module.css';

export function LabourUpdates({ labour }: { labour: LabourDTO }) {
  const [update, setUpdate] = useState('');
  const viewport = useRef<HTMLDivElement>(null);
  const auth = useAuth();
  const userName = auth.user?.profile.name;
  const completed = labour.end_time != null;
  const labourUpdates = labour.labour_updates;

  const labourUpdateDisplay = useMemo(() => {
    return labourUpdates.map((data) => {
      return <LabourUpdate data={data} completed={completed} owner />;
    });
  }, [labourUpdates, userName, completed]);

  useEffect(() => {
    if (viewport.current) {
      viewport.current.scrollTo({ top: viewport.current.scrollHeight, behavior: 'auto' });
    }
  }, [labourUpdates]);

  const handleUpdateChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    setUpdate(event.currentTarget.value);
  }, []);

  const title = completed ? 'Your labour updates' : 'Post an update';
  const completedDescription =
    'Here you can see the updates you made during your labour experience.';
  const activeDescription =
    'Share updates here to let your subscribers know how you are getting on. Making an announcement will send your update to your subscribers by their preferred methods.';

  return (
    <div className={baseClasses.root} style={{ maxHeight: 'calc(80% - 120px)' }}>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <ResponsiveTitle title={title} />
            <Text c="var(--mantine-color-gray-7)" mt="sm" mb="md">
              {completed ? completedDescription : activeDescription}
            </Text>
            {labourUpdateDisplay.length > 0 && (
              <ScrollArea.Autosize mah="55svh" viewportRef={viewport}>
                <div className={classes.statusUpdateContainer}>{labourUpdateDisplay}</div>
              </ScrollArea.Autosize>
            )}
            {labourUpdateDisplay.length === 0 && !completed && (
              <>
                <div className={classes.imageFlexRow}>
                  <Image src={image} className={classes.image} />
                </div>
                <ImportantText message="You haven't posted any updates yet." />
              </>
            )}
            {!completed && (
              <>
                <TextInput
                  mt={20}
                  rightSection={<IconPencil size={18} stroke={1.5} />}
                  radius="lg"
                  size="md"
                  visibleFrom="sm"
                  placeholder="What's happening with your labour?"
                  onChange={handleUpdateChange}
                  value={update}
                />
                <TextInput
                  mt={20}
                  rightSection={<IconPencil size={18} stroke={1.5} />}
                  radius="lg"
                  size="sm"
                  hiddenFrom="sm"
                  placeholder="What's happening with your labour?"
                  onChange={handleUpdateChange}
                  value={update}
                />
              </>
            )}
            <div className={classes.flexRow} style={{ marginTop: '10px' }}>
              {!completed && <PostStatusUpdateButton message={update} setUpdate={setUpdate} />}
              {!completed && (
                <MakeAnnouncementButton message={update} setAnnouncement={setUpdate} />
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
