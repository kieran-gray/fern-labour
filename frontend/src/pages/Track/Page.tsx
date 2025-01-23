import { Header } from "../../shared-components/Header/Header";
import { useAuth } from "react-oidc-context";
import { Container, Space, Title } from "@mantine/core";
import LabourContainer from "./Components/LabourContainer";
import SubscriptionsContainer from "./Components/SubscriptionsContainer";
import { FooterSimple } from "../../shared-components/Footer/Footer";

export const TrackPage: React.FC = () => {
  const auth = useAuth();
  const page = 'Home';

  return (
    <>
      <Header active={page} />
      <Container size={1200} p={15}>
        <div></div>
        <Title>Welcome, {auth.user?.profile.given_name}</Title>
        <Space h="xl" />
        <LabourContainer />
        <Space h="xl" />
        <SubscriptionsContainer />
      </Container>
      <FooterSimple />
    </>
  );
};
