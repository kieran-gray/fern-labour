import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Anchor, Box, Burger, Container, Drawer, Group, Space, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { MobileUserMenu, UserButton, UserMenu } from './UserMenu';
import classes from './Header.module.css';

const mainLinks = [
  { link: '/', label: 'Home' },
  { link: '/labour', label: 'Labour' },
  { link: '/share', label: 'Share' },
];

export function Header({ active }: { active: string }) {
  const [opened, { toggle }] = useDisclosure(false);
  const navigate = useNavigate();
  const auth = useAuth();

  const mainItems = mainLinks.map((item) => (
    <Anchor<'a'>
      href={item.link}
      key={item.label}
      className={classes.mainLink}
      data-active={item.label === active || undefined}
      onClick={(event) => {
        event.preventDefault();
        navigate(item.link);
      }}
    >
      {item.label}
    </Anchor>
  ));

  return (
    <header className={classes.header}>
      <Container className={classes.inner}>
        <div onClick={() => navigate('/')} className={classes.titleRow}>
          <img src="/logo/logo.svg" className={classes.icon} alt="Fern Icon" />
          <Text className={classes.title}>Fern Labour</Text>
        </div>
        <Box className={classes.links} visibleFrom="sm">
          <Group gap={30} justify="flex-end" className={classes.mainLinks}>
            {mainItems}
          </Group>
        </Box>
        <Group visibleFrom="sm">
          <UserMenu />
        </Group>
        <Drawer
          size="xs"
          classNames={{ content: classes.drawer, header: classes.drawer }}
          overlayProps={{ backgroundOpacity: 0.55, blur: 3 }}
          position="right"
          opened={opened}
          onClose={toggle}
        >
          <UserButton name={auth.user?.profile.name ?? ''} />
          <div className={classes.linksDrawer}>
            <Text className={classes.drawerLabel}>Navigation</Text>
            {mainItems}
            <Space h="xl" />
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
