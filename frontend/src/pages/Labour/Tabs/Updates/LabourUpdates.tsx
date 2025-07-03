import { useCallback, useEffect, useMemo, useRef } from 'react';
import { LabourDTO, LabourUpdateDTO } from '@clients/labour_service';
import { ImportantText } from '@shared/ImportantText/ImportantText';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { IconBook } from '@tabler/icons-react';
import { useAuth } from 'react-oidc-context';
import { ActionIcon, Image, ScrollArea } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import image from './image.svg';
import { LabourUpdate, LabourUpdateProps } from './LabourUpdate';
import { LabourUpdateControls } from './LabourUpdateControls';
import { LabourUpdatesHelpModal } from './Modals/HelpModal';
import classes from './LabourUpdates.module.css';
import baseClasses from '@shared/shared-styles.module.css';

interface LabourUpdatesProps {
  labour: LabourDTO;
}

const MESSAGES = {
  SHARED_LABOUR_BEGUN: (firstName: string) => `Exciting news, ${firstName} has started labour!`,
  PRIVATE_LABOUR_BEGUN:
    "You're now tracking contractions! Use the announce button on this message to let your subscribers know that labour has started!",
};

const mapLabourUpdateToProps = (
  update: LabourUpdateDTO,
  sharedLabourBegunMessage: string,
  privateLabourBegunMessage: string,
  completed: boolean
): LabourUpdateProps => {
  const sentTime = new Date(update.sent_time).toLocaleString().slice(0, 17).replace(',', ' at');
  switch (update.labour_update_type) {
    case 'announcement':
      if (update.application_generated) {
        return {
          id: update.id,
          sentTime,
          class: classes.privateNotePanel,
          icon: '🌱',
          badgeColor: '#ff8f00',
          badgeText: 'Fern Labour',
          text: sharedLabourBegunMessage,
          visibility: '📡 Broadcast to subscribers',
          showMenu: false,
          showFooter: true,
        };
      }
      return {
        id: update.id,
        sentTime,
        class: classes.announcementPanel,
        icon: '📣',
        badgeColor: 'var(--mantine-color-pink-6)',
        badgeText: update.labour_update_type.split('_')[0],
        text: update.message,
        visibility: '📡 Broadcast to subscribers',
        showMenu: false,
        showFooter: true,
      };

    case 'status_update':
      return {
        id: update.id,
        sentTime,
        class: classes.statusUpdatePanel,
        icon: '💫',
        badgeColor: '#24968b',
        badgeText: update.labour_update_type.split('_')[0],
        text: update.message,
        visibility: '👁️ Visible to subscribers',
        showMenu: !completed,
        showFooter: true,
      };

    default:
      return {
        id: update.id,
        sentTime,
        class: classes.privateNotePanel,
        icon: '🌱',
        badgeColor: '#ff8f00',
        badgeText: 'Fern Labour',
        text: privateLabourBegunMessage,
        visibility: '🔒 Only visible to you',
        showMenu: !completed,
        showFooter: true,
      };
  }
};

export function LabourUpdates({ labour }: LabourUpdatesProps) {
  const [opened, { open, close }] = useDisclosure(false);
  const viewport = useRef<HTMLDivElement>(null);
  const auth = useAuth();
  const firstName = auth.user?.profile.given_name || '';
  const completed = labour.end_time != null;
  const labourUpdates = labour.labour_updates;

  const sharedLabourBegunMessage = useMemo(
    () => MESSAGES.SHARED_LABOUR_BEGUN(firstName),
    [firstName]
  );

  const privateLabourBegunMessage = MESSAGES.PRIVATE_LABOUR_BEGUN;

  const scrollToBottom = useCallback(() => {
    setTimeout(() => {
      if (viewport.current) {
        viewport.current.scrollTo({
          top: viewport.current.scrollHeight,
          behavior: 'smooth',
        });
      }
    }, 1);
  }, []);

  const labourUpdateDisplay = useMemo(() => {
    return labourUpdates.map((data) => {
      return (
        <LabourUpdate
          data={mapLabourUpdateToProps(
            data,
            sharedLabourBegunMessage,
            privateLabourBegunMessage,
            completed
          )}
          key={data.id}
        />
      );
    });
  }, [labourUpdates, firstName, completed]);

  useEffect(() => {
    scrollToBottom();
  }, [labourUpdates, scrollToBottom]);

  const title = completed ? 'Your labour updates' : 'Share an update';
  const description = completed
    ? 'Here you can see the updates you made during your labour experience.'
    : 'Share updates here to let your subscribers know how you are getting on. Click the book icon above for more info.';

  const hasUpdates = labourUpdateDisplay.length > 0;
  const showEmptyState = !hasUpdates && !completed;

  return (
    <div className={baseClasses.root} style={{ maxHeight: 'calc(80% - 120px)' }}>
      <div className={baseClasses.body}>
        <div className={classes.titleRow}>
          <div className={classes.title} style={{ paddingBottom: 0 }}>
            <ResponsiveTitle title={title} />
          </div>
          <ActionIcon radius="xl" variant="light" size="xl" onClick={open}>
            <IconBook />
          </ActionIcon>
          <LabourUpdatesHelpModal close={close} opened={opened} />
        </div>
        <div className={baseClasses.inner} style={{ paddingTop: 0 }}>
          <div className={classes.content}>
            <ResponsiveDescription description={description} marginTop={0} />
            {hasUpdates && (
              <ScrollArea.Autosize mt={20} mah="55svh" viewportRef={viewport}>
                <div className={classes.statusUpdateContainer}>{labourUpdateDisplay}</div>
              </ScrollArea.Autosize>
            )}
            {showEmptyState && (
              <>
                <div className={classes.imageFlexRow}>
                  <Image src={image} className={classes.image} />
                </div>
                <ImportantText message="You haven't posted any updates yet." />
              </>
            )}
            {!completed && <LabourUpdateControls />}
          </div>
        </div>
      </div>
    </div>
  );
}
