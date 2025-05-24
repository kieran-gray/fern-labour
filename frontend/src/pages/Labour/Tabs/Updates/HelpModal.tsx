import { Modal, Space, Text, Title } from '@mantine/core';
import { LabourUpdate, LabourUpdateProps } from './LabourUpdate';
import modalClasses from '../../../../shared-components/Modal.module.css';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import labourUpdateClasses from './LabourUpdates.module.css';

type CloseFunctionType = (...args: any[]) => void;

export const LabourUpdatesHelpModal = ({
  opened,
  close,
}: {
  opened: boolean;
  close: CloseFunctionType;
}) => {
  const sentTime = new Date().toLocaleString().slice(0, 17).replace(',', ' at');
  const mockStatusUpdate: LabourUpdateProps = {
    id: 'mock-status-update',
    sentTime,
    class: labourUpdateClasses.statusUpdatePanel,
    icon: '💫',
    badgeColor: '#24968b',
    badgeText: 'status',
    text: "This is a status update, use me to make less important/urgent updates or just to say 'No, the baby is not here yet'",
    visibility: '👁️ Visible to subscribers',
    showMenu: true,
    showFooter: true,
  };
  const mockAnnouncement: LabourUpdateProps = {
    id: 'mock-status-update',
    sentTime,
    class: labourUpdateClasses.announcementPanel,
    icon: '📣',
    badgeColor: 'var(--mantine-color-primary-6)',
    badgeText: 'announcement',
    text: 'This is an announcement, use me to make more important updates',
    visibility: '📡 Broadcast to subscribers',
    showMenu: false,
    showFooter: true,
  };
  const mockLabourBegun: LabourUpdateProps = {
    id: 'mock-status-update',
    sentTime,
    class: labourUpdateClasses.privateNotePanel,
    icon: '🌱',
    badgeColor: '#ff8f00',
    badgeText: 'Fern Labour',
    text: "You're now tracking contractions! Use the announce button on this message to let your subscribers know that labour has started!",
    visibility: '🔒 Only visible to you',
    showMenu: true,
    showFooter: true,
  };
  return (
    <Modal
      opened={opened}
      onClose={close}
      title="What's this?"
      size="xl"
      transitionProps={{ transition: 'slide-left' }}
      overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
      classNames={{
        content: modalClasses.helpModalRoot,
        header: modalClasses.modalHeader,
        title: modalClasses.modalTitle,
        body: modalClasses.modalBody,
        close: modalClasses.closeButton,
      }}
    >
      <div
        className={baseClasses.inner}
        style={{ flexDirection: 'column', paddingLeft: '5px', paddingRight: '5px' }}
      >
        <Title order={3} visibleFrom="md">
          Sharing updates
        </Title>
        <Title order={4} mt="xs" hiddenFrom="md">
          Sharing updates
        </Title>
        <Text mt={10} size="sm" c="var(--mantine-color-gray-8)">
          You can share two different types of updates here to keep your loved ones updated.
          <br />
          <br />
          <Text fw={500} size="sm">
            Status updates
          </Text>
          Your subscribers can see status updates in the app but are not notified.
          <br />
          The menu on the lower right hand side of the message allows you to do some basic actions,
          such as sharing the message as an announcement or deleting it.
          <Space h="sm" />
          <LabourUpdate data={mockStatusUpdate} />
          <br />
          <br />
          <Text fw={500} size="sm">
            Announcements
          </Text>
          Announcements are broadcast by SMS/WhatsApp/email to any subscribers that have upgraded
          their subscription for live notifications.
          <Space h="sm" />
          <LabourUpdate data={mockAnnouncement} />
          <br />
          <br />
          <Text fw={500} size="sm">
            Application generated messages
          </Text>
          Sometimes we will generate messages that only you can see, we'll do this when you start
          tracking your contractions. Then you can choose if you want to share the message that your
          labour is beginning with your subscribers.
          <Space h="sm" />
          <LabourUpdate data={mockLabourBegun} />
          <br />
        </Text>
      </div>
    </Modal>
  );
};
