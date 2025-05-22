import { Title } from '@mantine/core';

interface ResponsiveTitleProps {
  title: string;
}

export function ResponsiveTitle({ title }: ResponsiveTitleProps) {
  return (
    <>
      <Title order={4} hiddenFrom="xs">
        {title}
      </Title>
      <Title order={3} hiddenFrom="sm" visibleFrom="xs">
        {title}
      </Title>
      <Title order={2} visibleFrom="sm">
        {title}
      </Title>
    </>
  );
}
