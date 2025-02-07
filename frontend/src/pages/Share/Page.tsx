import { Center, Space } from '@mantine/core';
import { FooterSimple } from '../../shared-components/Footer/Footer';
import { Header } from '../../shared-components/Header/Header';
import { InviteContainer } from './Components/InviteContainer/InviteContainer';
import { ShareContainer } from './Components/ShareContainer/ShareContainer';
import { SubscribersContainer } from './Components/SubscribersContainer/SusbcribersContainer';
import classes from '../../shared-components/shared-styles.module.css';

export const ShareBirthingPersonPage = () => {
  const page = 'Share';
  return (
    <div style={{ height: '100svh', display: 'flex', flexDirection: 'column' }}>
      <Header active={page} />
      <Center flex="shrink" p={15}>
        <div className={classes.flexColumn}>
          <SubscribersContainer />
          <InviteContainer />
          <Space h="xl" />
          <ShareContainer />
        </div>
      </Center>
      <div style={{ flexGrow: 1 }} />
      <FooterSimple />
    </div>
  );
};
