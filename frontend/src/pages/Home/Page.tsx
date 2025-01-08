import { Header } from "../../shared-components/Header/Header";
import { useAuth } from "react-oidc-context";
import { Container, Space, Title } from "@mantine/core";
import LabourContainer from "./Components/LabourContainer";
import SubscriptionsContainer from "./Components/SubscriptionsContainer";

export const HomePage: React.FC = () => {
  const auth = useAuth();
  const page = 'Home';

  return (
    <div>
      <Header active={page} />
      <Container size={1200} p={15}>
        <div></div>
        <Title>Welcome, {auth.user?.profile.given_name}</Title>
        <Space h="xl" />
        <LabourContainer />
        <Space h="xl" />
        <SubscriptionsContainer />
      </Container>
    </div>
  );
};
