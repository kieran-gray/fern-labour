import { forwardRef, useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { AppMode, useMode } from '@base/contexts/AppModeContext';
import {
  IconArrowLeft,
  IconHistory,
  IconHome,
  IconLogout,
  IconMessageCircleQuestion,
  IconMoon,
  IconPassword,
  IconSettings,
  IconSun,
  IconSwitchHorizontal,
  IconTrash,
} from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import {
  Avatar,
  Button,
  Group,
  SegmentedControl,
  Space,
  Text,
  UnstyledButton,
  useMantineColorScheme,
} from '@mantine/core';
import classes from './Header.module.css';

interface UserButtonProps extends React.ComponentPropsWithoutRef<'button'> {
  name: string;
  icon?: React.ReactNode;
}

export const UserButton = forwardRef<HTMLButtonElement, UserButtonProps>(
  ({ name, icon, ...others }: UserButtonProps, ref) => (
    <UnstyledButton ref={ref} className={classes.userButton} {...others}>
      <Group>
        <Avatar
          radius="xl"
          color="light-dark(var(--mantine-color-dark-6), var(--mantine-color-gray-4))"
        />
        <div style={{ flex: 1 }}>
          <Text
            size="sm"
            fw={500}
            c="light-dark(var(--mantine-color-dark-2), var(--mantine-color-gray-3))"
          >
            {name}
          </Text>
        </div>
        {icon}
      </Group>
    </UnstyledButton>
  )
);

export function MobileUserMenu() {
  const [section, setSection] = useState<'app' | 'account'>('app');
  const { user, loginWithRedirect, logout } = useAuth0();
  const navigate = useNavigate();
  const pathname = window.location.pathname;
  const { mode, setMode } = useMode();
  const switchToMode = mode === AppMode.Birth ? AppMode.Subscriber : AppMode.Birth;
  const { colorScheme, setColorScheme } = useMantineColorScheme();

  const themeIcon =
    colorScheme === 'light' ? (
      <IconMoon size={16} stroke={1.5} />
    ) : (
      <IconSun size={16} stroke={1.5} />
    );

  const appSettings = (
    <Group>
      <Space h="xs" />
      <Button
        key="theme"
        className={classes.mainLink}
        onClick={() => setColorScheme(colorScheme === 'light' ? 'dark' : 'light')}
        leftSection={themeIcon}
        size="md"
        w="100%"
        variant="transparent"
      >
        {colorScheme === 'light' ? 'Night Mode' : 'Day Mode'}
      </Button>
      {mode === null && pathname !== '/' && (
        <Button
          key="home"
          className={classes.mainLink}
          onClick={() => {
            navigate('/');
          }}
          leftSection={<IconHome size={16} stroke={1.5} />}
          size="md"
          w="100%"
          variant="transparent"
        >
          Home
        </Button>
      )}
      {mode !== null && (
        <>
          <Button
            key="update"
            className={classes.mainLink}
            onClick={() => {
              setMode(switchToMode);
              navigate('/');
            }}
            leftSection={<IconSwitchHorizontal size={16} stroke={1.5} />}
            size="md"
            w="100%"
            variant="transparent"
          >
            Switch to {switchToMode} Mode
          </Button>
          {mode === AppMode.Birth && ['/history', '/contact'].includes(pathname) && (
            <Button
              key="history"
              onClick={() => navigate('/')}
              leftSection={<IconArrowLeft size={16} stroke={1.5} />}
              className={classes.mainLink}
              size="md"
              w="100%"
              variant="transparent"
            >
              Go to your labour
            </Button>
          )}
          {mode === AppMode.Birth && pathname !== '/history' && (
            <Button
              key="labour"
              onClick={() => navigate('/history')}
              className={classes.mainLink}
              leftSection={<IconHistory size={16} stroke={1.5} />}
              size="md"
              w="100%"
              variant="transparent"
            >
              Your Labour History
            </Button>
          )}
        </>
      )}
    </Group>
  );

  const accountSettings = (
    <>
      <Group>
        <Space h="xs" />
        <Button
          key="update"
          className={classes.mainLink}
          onClick={(event) => {
            event.preventDefault();
            void loginWithRedirect({
              authorizationParams: { kc_action: 'UPDATE_PROFILE' },
            });
          }}
          leftSection={<IconSettings size={16} stroke={1.5} />}
          size="md"
          w="100%"
          variant="transparent"
        >
          Update Profile
        </Button>
        <Button
          key="password"
          className={classes.mainLink}
          onClick={(event) => {
            event.preventDefault();
            void loginWithRedirect({
              authorizationParams: { kc_action: 'UPDATE_PASSWORD' },
            });
          }}
          leftSection={<IconPassword size={16} stroke={1.5} />}
          size="md"
          w="100%"
          variant="transparent"
        >
          Change Password
        </Button>
        <Button
          key="delete"
          className={classes.mainLink}
          onClick={(event) => {
            event.preventDefault();
            void loginWithRedirect({
              authorizationParams: { kc_action: 'delete_account' },
            });
          }}
          leftSection={<IconTrash size={16} stroke={1.5} />}
          size="md"
          w="100%"
          variant="transparent"
        >
          Delete Account
        </Button>
      </Group>
    </>
  );

  const links = section === 'app' ? appSettings : accountSettings;

  return (
    <div className={classes.linksDrawer}>
      <SegmentedControl
        value={section}
        onChange={(value: any) => setSection(value)}
        transitionTimingFunction="ease"
        fullWidth
        data={[
          { label: 'App', value: 'app' },
          { label: 'Account Settings', value: 'account' },
        ]}
        radius="lg"
        mt={0}
        color="var(--mantine-primary-color-4)"
        styles={{
          root: {
            backgroundColor:
              'light-dark(var(--mantine-primary-color-1), var(--mantine-color-primary-8))',
          },
        }}
      />

      {links}

      <div style={{ flexGrow: 1 }} />
      <div className={classes.footer}>
        <UserButton name={user?.name ?? ''} />
        <Button
          key="logout"
          className={classes.mainLink}
          onClick={(event) => {
            event.preventDefault();
            void logout({ logoutParams: { returnTo: window.location.origin } });
          }}
          size="md"
          w="100%"
          variant="transparent"
          leftSection={<IconLogout size={16} stroke={1.5} />}
        >
          Logout
        </Button>
        {pathname !== '/contact' && (
          <Button
            key="contact"
            onClick={() => navigate('/contact')}
            className={classes.mainLink}
            leftSection={<IconMessageCircleQuestion size={16} stroke={1.5} />}
            size="md"
            w="100%"
            variant="transparent"
            mt={10}
          >
            Contact Us
          </Button>
        )}
      </div>
    </div>
  );
}
