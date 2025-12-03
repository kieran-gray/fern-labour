import { List, Modal, Stack, Text, Title } from '@mantine/core';
import { LabourUpdate, LabourUpdateProps } from '../LabourUpdate';
import labourUpdateClasses from '../LabourUpdates.module.css';
import modalClasses from '@shared/Modal.module.css';
import baseClasses from '@shared/shared-styles.module.css';

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
    badgeColor: 'var(--mantine-primary-color-6)',
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
        style={{
          flexDirection: 'column',
          paddingLeft: '5px',
          paddingRight: '5px',
          color: 'light-dark(var(--mantine-color-gray-9), var(--mantine-color-gray-0))',
        }}
      >
        <Title order={3} visibleFrom="md">
          Sharing updates
        </Title>
        <Title order={4} mt="xs" hiddenFrom="md">
          Sharing updates
        </Title>
        <Stack gap="sm" mt={10}>
          <Text size="sm" c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))">
            Share updates to keep loved ones in the loop. There are two types you can send, plus
            occasional app messages just for you:
          </Text>

          <Text
            fw={500}
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
          >
            Status updates
          </Text>
          <List
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
            withPadding
          >
            <List.Item>
              Visible to subscribers inside the app (no push/SMS/WhatsApp/email)
            </List.Item>
            <List.Item>
              Use the message menu (bottom-right) to edit, share as an announcement, or delete
            </List.Item>
          </List>
          <LabourUpdate data={mockStatusUpdate} />

          <Text
            fw={500}
            size="sm"
            mt="xs"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
          >
            Announcements
          </Text>
          <List
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
            withPadding
          >
            <List.Item>
              Broadcast to subscribers via SMS/WhatsApp/email who have live notifications enabled
            </List.Item>
            <List.Item>Best for important updates</List.Item>
          </List>
          <LabourUpdate data={mockAnnouncement} />

          <Text
            fw={500}
            size="sm"
            mt="xs"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
          >
            Application‑generated messages
          </Text>
          <List
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
            withPadding
          >
            <List.Item>Private to you (not visible to subscribers)</List.Item>
            <List.Item>
              Created automatically at key moments, e.g., when you start tracking contractions
            </List.Item>
            <List.Item>You can choose to share as an announcement</List.Item>
          </List>
          <LabourUpdate data={mockLabourBegun} />
        </Stack>
      </div>
    </Modal>
  );
};
