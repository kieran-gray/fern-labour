import { IconCheck, IconCopy } from '@tabler/icons-react';
import { Button, Tooltip } from '@mantine/core';
import { useClipboard } from '@mantine/hooks';

export function CopyButton({text}: {text: string}) {
  const clipboard = useClipboard();
  return (
    <Tooltip
      label="Link copied!"
      offset={5}
      position="bottom"
      radius="xl"
      transitionProps={{ duration: 100, transition: 'slide-down' }}
      opened={clipboard.copied}
    >
      <Button
        color='var(--mantine-color-pink-4)'
        variant="filled"
        rightSection={
          clipboard.copied ? (
            <IconCheck size={20} stroke={1.5} />
          ) : (
            <IconCopy size={20} stroke={1.5} />
          )
        }
        radius="xl"
        size="md"
        pr={14}
        h={48}
        mt={'var(--mantine-spacing-lg)'}
        styles={{ section: { marginLeft: 22 } }}
        onClick={() => clipboard.copy(text)}
      >
        Copy share link to clipboard
      </Button>
    </Tooltip>
  );
}