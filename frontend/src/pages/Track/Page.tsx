import { useAuth } from 'react-oidc-context';
import { Container, Space, Title } from '@mantine/core';
import { FooterSimple } from '../../shared-components/Footer/Footer';
import { Header } from '../../shared-components/Header/Header';
import LabourContainer from './Components/LabourContainer';
import SubscriptionsContainer from './Components/SubscriptionsContainer';

export const TrackPage: React.FC = () => {
  const auth = useAuth();
  const page = 'Home';

  return (
    <div style={{ height: '100svh', display: 'flex', flexDirection: 'column' }}>
      <Header active={page} />
      <Container size={1200} p={15}>
        <div />
        <Title>Welcome, {auth.user?.profile.given_name}</Title>
        <Space h="xl" />
        <LabourContainer />
        <Space h="xl" />
        <SubscriptionsContainer />
      </Container>
      <div style={{ flexGrow: 1 }} />
      <FooterSimple />
    </div>
  );
};
