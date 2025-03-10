import { Center, Space } from '@mantine/core';
import { FooterSimple } from './Footer/Footer';
import { Header } from './Header/Header';

export const AppShell = ({ children }: { children: React.ReactNode }) => {
  return (
    <div style={{ height: '100svh', display: 'flex', flexDirection: 'column' }}>
      <Header />
      <Center flex="shrink" style={{ overflow: 'visible' }}>
        {children}
      </Center>
      <Space h="xl" />
      <div style={{ flexGrow: 1 }} />
      <FooterSimple />
    </div>
  );
};
