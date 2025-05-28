import { IconQrcode } from '@tabler/icons-react';
import { QRCodeSVG } from 'qrcode.react';
import { Button, Modal, Space } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import classes from '@shared/Modal.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export default function QRButton({ url }: { url: string }) {
  const [opened, { open, close }] = useDisclosure(false);
  const icon = <IconQrcode size={25} />;
  return (
    <>
      <Modal
        overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
        classNames={{
          content: classes.modalRoot,
          header: classes.modalHeader,
          title: classes.modalTitle,
          body: classes.modalBody,
          close: classes.closeButton,
        }}
        opened={opened}
        onClose={close}
        title="Your invite QR code"
      >
        <Space h="lg" />
        <div className={baseClasses.flexRow} style={{ width: '100%' }}>
          <QRCodeSVG
            value={url}
            style={{ width: '70%', height: '70%', margin: 'auto' }}
            bgColor="light-dark(var(--mantine-color-white), var(--mantine-color-primary-2))"
            fgColor="light-dark(var(--mantine-primary-color-9), var(--mantine-primary-color-0)"
          />
        </div>
        <Space h="lg" />
      </Modal>
      <Button
        leftSection={icon}
        radius="xl"
        size="lg"
        variant="outline"
        onClick={open}
        mt="var(--mantine-spacing-lg)"
        visibleFrom="sm"
      >
        QR Code
      </Button>
      <Button
        leftSection={icon}
        radius="xl"
        size="md"
        h={48}
        variant="outline"
        onClick={open}
        mt="var(--mantine-spacing-sm)"
        hiddenFrom="sm"
      >
        QR Code
      </Button>
    </>
  );
}
