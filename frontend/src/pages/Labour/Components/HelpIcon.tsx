import { IconHelp } from '@tabler/icons-react';
import { ActionIcon } from '@mantine/core';

export function HelpIcon() {
  return (
    <ActionIcon variant="transparent" color="rgba(255, 255, 255, 1)" aria-label="Settings">
      <IconHelp style={{ width: '80%', height: '80%' }} stroke={1.5} />
    </ActionIcon>
  );
}
