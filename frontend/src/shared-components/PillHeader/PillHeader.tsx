import { IconChevronDown, IconSettings } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import {
  ActionIcon,
  Burger,
  Button,
  Container,
  Drawer,
  Flex,
  Group,
  Menu,
  Text,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { MobileUserMenu } from '../Header/UserMenu';
import classes from './PillHeader.module.css';

interface NavItem {
  id: string;
  label: string;
  icon: React.ComponentType<any>;
  requiresPaid?: boolean;
}

interface PillHeaderProps {
  navItems?: readonly NavItem[];
  activeNav?: string | null;
  onNavChange?: (nav: string) => void;
}

export function PillHeader({ navItems, activeNav, onNavChange }: PillHeaderProps) {
  const [mobileOpened, { toggle: toggleMobile }] = useDisclosure(false);
  const [desktopOpened, { toggle: toggleDesktop }] = useDisclosure(false);
  const [menuOpened, { toggle: toggleMenu }] = useDisclosure(false);
  const navigate = useNavigate();

  return (
    <Container
      className={classes.container}
      component="header"
      mt="10px"
      mx={{ base: '15px', sm: 'auto' }}
      w={{ base: 'auto', sm: "95%" }}
      maw={{ sm: 1050 }}
      h={60}
    >
      <Flex
        justify="space-between"
        align="center"
        h="100%"
        style={{ overflow: 'hidden' }}
        gap="lg"
        wrap="nowrap"
      >
        {/* Left: Burger + Logo */}
        <Group gap={0} style={{ flexShrink: 0 }}>
          <Burger
            size="sm"
            opened={mobileOpened}
            onClick={toggleMobile}
            hiddenFrom="sm"
            color="var(--mantine-color-white)"
            title="Navigation Menu"
          />
          <div onClick={() => navigate('/')} className={classes.logoContainer}>
            <img src="/logo/logo.svg" className={classes.icon} alt="Fern Logo" />
            <Text className={classes.title}>Fern Labour</Text>
          </div>
        </Group>

        {/* Mobile Drawer */}
        <Drawer
          size="xs"
          classNames={{
            content: classes.drawer,
            header: classes.drawer,
            body: classes.drawerBody,
          }}
          overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
          position="left"
          opened={mobileOpened}
          onClose={toggleMobile}
        >
          <MobileUserMenu />
        </Drawer>

        {/* Desktop Drawer */}
        <Drawer
          size="xs"
          classNames={{
            content: classes.drawer,
            header: classes.drawer,
            body: classes.drawerBody,
          }}
          overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
          position="right"
          opened={desktopOpened}
          onClose={toggleDesktop}
        >
          <MobileUserMenu />
        </Drawer>

        {/* Center: Navigation Menu (Desktop Only) */}
        {navItems && navItems.length > 0 && (
          <Group gap="md" style={{ flexShrink: 0 }} visibleFrom="sm">
            <Menu
              opened={menuOpened}
              onChange={toggleMenu}
              position="bottom"
              withArrow
              offset={5}
              classNames={{
                dropdown: classes.menuDropdown,
                item: classes.menuItem,
              }}
            >
              <Menu.Target>
                <Button
                  variant="subtle"
                  color="white"
                  size="sm"
                  radius="xl"
                  className={classes.navButton}
                  rightSection={<IconChevronDown size={16} />}
                >
                  {navItems.find((item) => item.id === activeNav)?.label || 'Navigate'}
                </Button>
              </Menu.Target>
              <Menu.Dropdown>
                {navItems.map(({ id, label, icon: Icon }) => (
                  <Menu.Item
                    key={id}
                    leftSection={<Icon size={16} stroke={1.5} />}
                    onClick={() => onNavChange?.(id)}
                    className={activeNav === id ? classes.menuItemActive : ''}
                  >
                    {label}
                  </Menu.Item>
                ))}
              </Menu.Dropdown>
            </Menu>
          </Group>
        )}

        {/* Right: Settings Button */}
        <Group gap="sm" style={{ flexShrink: 0 }}>
          <ActionIcon
            variant="subtle"
            color="white"
            size="lg"
            radius="xl"
            visibleFrom="sm"
            className={classes.userAction}
            onClick={toggleDesktop}
            title="Options"
          >
            <IconSettings size={20} />
          </ActionIcon>
        </Group>
      </Flex>
    </Container>
  );
}
