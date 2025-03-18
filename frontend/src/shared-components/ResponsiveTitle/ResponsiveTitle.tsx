import { Title } from '@mantine/core';

interface ResponsiveTitleProps {
  title: string;
}

export function ResponsiveTitle({ title }: ResponsiveTitleProps) {
  return (
    <>
      <Title order={3} hiddenFrom="sm">
        {title}
      </Title>
      <Title order={2} visibleFrom="sm">
        {title}
      </Title>
    </>
  );
}
