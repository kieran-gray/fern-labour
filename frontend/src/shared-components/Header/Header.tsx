import { useNavigate } from 'react-router-dom';
import { Burger, Container, Drawer, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { MobileUserMenu } from './UserMenu';
import classes from './Header.module.css';

export function Header() {
  const [opened, { toggle }] = useDisclosure(false);
  const navigate = useNavigate();

  return (
    <header className={classes.header}>
      <Container className={classes.inner} size="lg">
        <Burger
          opened={opened}
          onClick={toggle}
          className={classes.burger}
          size="sm"
          color="white"
          hiddenFrom="sm"
        />
        <div onClick={() => navigate('/')} className={classes.titleRow}>
          <img src="/logo/logo.svg" className={classes.icon} alt="Fern Icon" />
          <Text className={classes.title}>Fern Labour</Text>
        </div>
        <Burger
          opened={opened}
          onClick={toggle}
          className={classes.burger}
          size="sm"
          color="white"
          visibleFrom="sm"
        />
        <Drawer
          size="xs"
          classNames={{ content: classes.drawer, header: classes.drawer, body: classes.body }}
          overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
          position="left"
          opened={opened}
          onClose={toggle}
        >
          <MobileUserMenu />
        </Drawer>
      </Container>
    </header>
  );
}
