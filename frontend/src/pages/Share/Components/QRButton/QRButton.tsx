import { Button, Modal, Space } from '@mantine/core';
import { IconQrcode } from '@tabler/icons-react';
import classes from './Modal.module.css'
import {QRCodeSVG} from 'qrcode.react';
import { useDisclosure } from '@mantine/hooks';
import baseClasses from '../../../../shared-components/shared-styles.module.css'

export default function QRButton({url}: {url: string}) {
    const [opened, { open, close }] = useDisclosure(false);
    const icon = <IconQrcode size={25} />;
    return (
        <>
            <Modal
                overlayProps={{ backgroundOpacity: 0.55, blur: 3 }}
                classNames={
                    {
                        content: classes.root,
                        header:classes.modalHeader,
                        title: classes.modalTitle,
                        body:classes.modalBody,
                        close: classes.closeButton
                    }
                }
                opened={opened}
                onClose={close}
                title="Your share QR code"
            >
                <Space h="lg"></Space>
                <div className={baseClasses.flexRow}>
                    <QRCodeSVG
                        value={url}
                        className={classes.qrCode}
                        bgColor='var(--mantine-color-pink-0)'
                        fgColor='var(--mantine-color-pink-9)'
                    />
                </div >
                <Space h="lg"></Space>
            </Modal>
            <Button
                leftSection={icon}
                radius="xl"
                size='lg'
                variant="outline"
                onClick={open}
                mt={'var(--mantine-spacing-lg)'}
            >
                QR Code
            </Button>
        </>
    )
}
