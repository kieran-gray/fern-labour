import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Burger, Container, Drawer, Group, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { MobileUserMenu, UserButton, UserMenu } from './UserMenu';
import classes from './Header.module.css';

export function Header() {
  const [opened, { toggle }] = useDisclosure(false);
  const navigate = useNavigate();
  const auth = useAuth();

  return (
    <header className={classes.header}>
      <Container className={classes.inner} size="lg">
        <div onClick={() => navigate('/')} className={classes.titleRow}>
          <img src="/logo/logo.svg" className={classes.icon} alt="Fern Icon" />
          <Text className={classes.title}>Fern Labour</Text>
        </div>
        <Group visibleFrom="sm">
          <UserMenu />
        </Group>
        <Drawer
          size="xs"
          classNames={{ content: classes.drawer, header: classes.drawer }}
          overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
          position="right"
          opened={opened}
          onClose={toggle}
        >
          <UserButton name={auth.user?.profile.name ?? ''} />
          <div className={classes.linksDrawer}>
            <MobileUserMenu />
          </div>
        </Drawer>
        <Burger
          opened={opened}
          onClick={toggle}
          className={classes.burger}
          size="sm"
          hiddenFrom="sm"
          color="white"
        />
      </Container>
    </header>
  );
}
