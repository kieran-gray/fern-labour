import { Header } from '../../shared-components/Header/Header';
import { ShareContainer } from './Components/ShareContainer/ShareContainer';
import { Center, Space } from '@mantine/core';
import { InviteContainer } from './Components/InviteContainer/InviteContainer';
import classes from '../../shared-components/shared-styles.module.css'
import { SubscribersContainer } from './Components/SubscribersContainer/SusbcribersContainer';
import { FooterSimple } from '../../shared-components/Footer/Footer';

export const ShareBirthingPersonPage = () => {
  const page = 'Share';
  return (
    <div style={{height: '100svh', display: 'flex', flexDirection: 'column'}}>
      <Header active={page}/>
      <Center flex={"shrink"}  p={15}>
        <div className={classes.flexColumn}>
          <SubscribersContainer />
          <InviteContainer />
          <Space h={"xl"} />
          <ShareContainer />
        </div>
      </Center>
      <div style={{flexGrow: 1}}></div>
      <FooterSimple />
    </div>
  );
};
