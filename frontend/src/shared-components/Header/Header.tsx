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
        <div onClick={() => navigate('/')} className={classes.titleRow}>
          <img src="/logo/logo.svg" className={classes.icon} alt="Fern Icon" />
          <Text className={classes.title}>Fern Labour</Text>
        </div>
        <Drawer
          size="xs"
          classNames={{ content: classes.drawer, header: classes.drawer, body: classes.body }}
          overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
          position="right"
          opened={opened}
          onClose={toggle}
        >
          <MobileUserMenu />
        </Drawer>
        <Burger
          opened={opened}
          onClick={toggle}
          className={classes.burger}
          size="sm"
          color="white"
        />
      </Container>
    </header>
  );
}
