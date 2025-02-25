import { forwardRef } from 'react';
import {
  IconChevronRight,
  IconLogout,
  IconPassword,
  IconSettings,
  IconSwitchHorizontal,
  IconTrash,
} from '@tabler/icons-react';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Anchor, Avatar, Group, Menu, Space, Text, UnstyledButton } from '@mantine/core';
import { AppMode, useMode } from '../../pages/Home/SelectAppMode';
import classes from './Header.module.css';

interface UserButtonProps extends React.ComponentPropsWithoutRef<'button'> {
  name: string;
  icon?: React.ReactNode;
}

export const UserButton = forwardRef<HTMLButtonElement, UserButtonProps>(
  ({ name, icon, ...others }: UserButtonProps, ref) => (
    <UnstyledButton ref={ref} className={classes.userButton} {...others}>
      <Group>
        <Avatar radius="xl" color="var(--mantine-color-white)" />
        <div style={{ flex: 1 }}>
          <Text size="sm" fw={500} c="var(--mantine-color-white)">
            {name}
          </Text>
        </div>
        {icon}
      </Group>
    </UnstyledButton>
  )
);

export function UserMenu() {
  const auth = useAuth();
  const navigate = useNavigate();
  const { mode, setMode } = useMode();
  const switchToMode = mode === AppMode.Birth ? AppMode.Subscriber : AppMode.Birth;

  return (
    <Group justify="center">
      <Menu withArrow position="bottom" transitionProps={{ transition: 'pop' }} withinPortal>
        <Menu.Target>
          <UserButton
            name={auth.user?.profile.name ?? ''}
            icon={<IconChevronRight size={16} color="var(--mantine-color-white)" />}
          />
        </Menu.Target>
        <Menu.Dropdown>
          {mode !== null && (
            <>
              <Menu.Label>Current Mode: {mode}</Menu.Label>
              <Menu.Item
                leftSection={<IconSwitchHorizontal size={16} stroke={1.5} />}
                onClick={() => {
                  setMode(switchToMode);
                  navigate('/');
                }}
              >
                Switch to {switchToMode} mode
              </Menu.Item>
            </>
          )}
          <Menu.Label>Settings</Menu.Label>
          <Menu.Item
            leftSection={<IconSettings size={16} stroke={1.5} />}
            onClick={() => {
              auth.signinRedirect({ extraQueryParams: { kc_action: 'UPDATE_PROFILE' } });
            }}
          >
            Update Profile
          </Menu.Item>
          <Menu.Item
            leftSection={<IconPassword size={16} stroke={1.5} />}
            onClick={() => {
              auth.signinRedirect({ extraQueryParams: { kc_action: 'UPDATE_PASSWORD' } });
            }}
          >
            Change Password
          </Menu.Item>
          <Menu.Item
            leftSection={<IconLogout size={16} stroke={1.5} />}
            onClick={() => {
              void auth.signoutRedirect();
            }}
          >
            Logout
          </Menu.Item>

          <Menu.Divider />

          <Menu.Label>Danger zone</Menu.Label>
          <Menu.Item
            color="red"
            leftSection={<IconTrash size={16} stroke={1.5} />}
            onClick={() => {
              auth.signinRedirect({ extraQueryParams: { kc_action: 'delete_account' } });
            }}
          >
            Delete account
          </Menu.Item>
        </Menu.Dropdown>
      </Menu>
    </Group>
  );
}

export function MobileUserMenu() {
  const auth = useAuth();
  const navigate = useNavigate();
  const { mode, setMode } = useMode();
  const switchToMode = mode === AppMode.Birth ? AppMode.Subscriber : AppMode.Birth;

  return (
    <>
      {mode !== null && (
        <>
          <Text className={classes.drawerLabel}>Current Mode: {mode}</Text>
          <Anchor<'a'>
            key="update"
            className={classes.mainLink}
            onClick={() => {
              setMode(switchToMode);
              navigate('/');
            }}
          >
            Switch to {switchToMode} Mode
          </Anchor>
        </>
      )}
      <Text className={classes.drawerLabel}>Settings</Text>
      <Anchor<'a'>
        key="update"
        className={classes.mainLink}
        onClick={(event) => {
          event.preventDefault();
          auth.signinRedirect({ extraQueryParams: { kc_action: 'UPDATE_PROFILE' } });
        }}
      >
        Update Profile
      </Anchor>
      <Anchor<'a'>
        key="password"
        className={classes.mainLink}
        onClick={(event) => {
          event.preventDefault();
          auth.signinRedirect({ extraQueryParams: { kc_action: 'UPDATE_PASSWORD' } });
        }}
      >
        Change Password
      </Anchor>
      <Anchor<'a'>
        key="logout"
        className={classes.mainLink}
        onClick={(event) => {
          event.preventDefault();
          void auth.signoutRedirect();
        }}
      >
        Logout
      </Anchor>
      <Space h="xl" />
      <Text className={classes.drawerLabel}>Danger Zone</Text>
      <Anchor<'a'>
        key="delete"
        className={classes.mainLink}
        onClick={(event) => {
          event.preventDefault();
          auth.signinRedirect({ extraQueryParams: { kc_action: 'delete_account' } });
        }}
        c="var(--mantine-color-pink-8)"
      >
        Delete Account
      </Anchor>
      <Space h="xl" />
    </>
  );
}
