import { Center, Space } from '@mantine/core';
import { Header } from './Header/Header';

export const AppShell = ({ children }: { children: React.ReactNode }) => {
  return (
    <div
      style={{
        minHeight: '100dvh',
        transition: 'min-height 10ms',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: 'var(--mantine-color-pink-0)',
      }}
    >
      <Header />
      <Center flex="shrink">{children}</Center>
      <Space h="md" />
      <div style={{ flexGrow: 1 }} />
    </div>
  );
};
