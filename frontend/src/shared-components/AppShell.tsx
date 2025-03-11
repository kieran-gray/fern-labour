import { Center, Space } from '@mantine/core';
import { FooterSimple } from './Footer/Footer';
import { Header } from './Header/Header';

export const AppShell = ({ children }: { children: React.ReactNode }) => {
  return (
    <div
      style={{
        minHeight: '100dvh',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: 'var(--mantine-color-pink-0)',
      }}
    >
      <Header />
      <Center flex="shrink">{children}</Center>
      <Space h="xl" />
      <div style={{ flexGrow: 1 }} />
      <FooterSimple />
    </div>
  );
};
