import { Header } from '../../shared-components/Header/Header';
import { ShareContainer } from './Components/ShareContainer/ShareContainer';
import { Center, Space } from '@mantine/core';
import { InviteContainer } from './Components/InviteContainer/InviteContainer';
import classes from '../../shared-components/shared-styles.module.css'
import { SubscribersContainer } from './Components/SubscribersContainer/SusbcribersContainer';

export const ShareBirthingPersonPage = () => {
  const page = 'Share';
  return (
    <div>
      <Header active={page}/>
      <Center flex={"shrink"}  p={15}>
        <div className={classes.flexColumn}>
          <SubscribersContainer />
          <InviteContainer />
          <Space h={"xl"} />
          <ShareContainer />
        </div>
      </Center>
    </div>
  );
};
