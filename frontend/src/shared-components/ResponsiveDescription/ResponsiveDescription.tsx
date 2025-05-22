import { Text } from '@mantine/core';

interface ResponsiveDescriptionProps {
  description: string | JSX.Element;
  marginTop: number;
}

export function ResponsiveDescription({ description, marginTop }: ResponsiveDescriptionProps) {
  return (
    <div style={{ marginTop }}>
      <Text size="sm" hiddenFrom="sm" c="var(--mantine-color-gray-8)">
        {description}
      </Text>
      <Text size="md" visibleFrom="sm" c="var(--mantine-color-gray-8)">
        {description}
      </Text>
    </div>
  );
}
