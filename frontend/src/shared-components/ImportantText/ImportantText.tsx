import { IconInfoCircle } from '@tabler/icons-react';
import { Text } from '@mantine/core';
import baseClasses from '../shared-styles.module.css';

export const ImportantText = ({ message }: { message: string }) => {
  return (
    <Text className={baseClasses.importantText}>
      <IconInfoCircle
        size={20}
        style={{ alignSelf: 'center', marginRight: '10px', flexShrink: 0 }}
      />
      {message}
    </Text>
  );
};
