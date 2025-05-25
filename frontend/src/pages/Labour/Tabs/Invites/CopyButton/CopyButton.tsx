import { IconCheck, IconCopy } from '@tabler/icons-react';
import { Button, Tooltip } from '@mantine/core';
import { useClipboard, useMediaQuery } from '@mantine/hooks';

export function CopyButton({ text }: { text: string }) {
  const clipboard = useClipboard();
  const isMobile = useMediaQuery('(min-width: 48em)');

  return (
    <>
      <Tooltip
        label="Link copied!"
        offset={5}
        position="bottom"
        radius="xl"
        transitionProps={{ duration: 100, transition: 'slide-down' }}
        opened={clipboard.copied}
        disabled={!isMobile}
        events={{ hover: true, focus: false, touch: true }}
      >
        <Button
          color="var(--mantine-primary-color-4)"
          variant="filled"
          rightSection={
            clipboard.copied ? (
              <IconCheck size={20} stroke={1.5} />
            ) : (
              <IconCopy size={20} stroke={1.5} />
            )
          }
          radius="xl"
          size="lg"
          pr={14}
          mt="var(--mantine-spacing-lg)"
          styles={{ section: { marginLeft: 22 } }}
          onClick={() => clipboard.copy(text)}
          visibleFrom="sm"
        >
          Copy to clipboard
        </Button>
      </Tooltip>
      <Tooltip
        label="Link copied!"
        offset={5}
        position="bottom"
        radius="xl"
        transitionProps={{ duration: 100, transition: 'slide-down' }}
        opened={clipboard.copied}
        disabled={isMobile}
        events={{ hover: true, focus: false, touch: true }}
      >
        <Button
          color="var(--mantine-primary-color-4)"
          variant="filled"
          rightSection={
            clipboard.copied ? (
              <IconCheck size={18} stroke={1.5} />
            ) : (
              <IconCopy size={18} stroke={1.5} />
            )
          }
          radius="xl"
          size="md"
          h={48}
          mt="var(--mantine-spacing-sm)"
          styles={{ section: { marginLeft: 18 } }}
          onClick={() => clipboard.copy(text)}
          hiddenFrom="sm"
        >
          Copy to clipboard
        </Button>
      </Tooltip>
    </>
  );
}
