import { Center, Space } from '@mantine/core';
import { PillHeader } from './PillHeader/PillHeader';

interface NavItem {
  id: string;
  label: string;
  icon: React.ComponentType<any>;
  requiresPaid?: boolean;
}

interface AppShellProps {
  children: React.ReactNode;
  navItems?: readonly NavItem[];
  activeNav?: string | null;
  onNavChange?: (nav: string) => void;
}

export const AppShell = ({ children, navItems, activeNav, onNavChange }: AppShellProps) => {
  return (
    <div
      style={{
        minHeight: '100dvh',
        transition: 'min-height 10ms',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: 'light-dark(#ffeae6, #121212)',
      }}
    >
      <PillHeader navItems={navItems} activeNav={activeNav} onNavChange={onNavChange} />
      <Center flex="shrink">{children}</Center>
      <Space h="md" />
      <div style={{ flexGrow: 1 }} />
    </div>
  );
};
