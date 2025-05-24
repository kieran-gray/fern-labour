import classes from '../shared-styles.module.css';
import { Text } from '@mantine/core';

interface ResponsiveDescriptionProps {
  description: string | JSX.Element;
  marginTop: number;
}

export function ResponsiveDescription({ description, marginTop }: ResponsiveDescriptionProps) {
  return (
    <div style={{ marginTop }}>
      <Text size="sm" hiddenFrom="sm" className={classes.description}>
        {description}
      </Text>
      <Text size="md" visibleFrom="sm" className={classes.description}>
        {description}
      </Text>
    </div>
  );
}
