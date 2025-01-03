import { useEffect, useState } from "react";
import { BirthingPersonSummaryDTO, BirthingPersonResponse, BirthingPersonDTO, GetSubscriptionsResponse } from "../../client";
import { Header } from "../../shared-components/Header/Header";
import { useAuth } from "react-oidc-context";
import Subscriptions from "./Components/Subscriptions";
import { PageLoading } from "../../shared-components/PageLoading/PageLoading";
import { Container, Space, Title } from "@mantine/core";
import Labours from "./Components/Labours";
import ContactMethodsModal from "../../shared-components/ContactMethodsModal/ContactMethodsModal";

export const HomePage: React.FC = () => {
  const [birthingPerson, setBirthingPerson] = useState<BirthingPersonDTO | null>(null);
  const [subscriptions, setSubscriptions] = useState<BirthingPersonSummaryDTO[]>([]);
  const [promptForSubscriberRegistration, setPromptForSubscriberRegistration] = useState<boolean>(false)
  const [newUser, setNewUser] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const auth = useAuth();
  const page = 'Home';

  const headers = {
    'Authorization': `Bearer ${auth.user?.access_token}`
  }

  const registerBirthingPerson = async (): Promise<BirthingPersonDTO | null> => {
    const response = await fetch(
      'http://localhost:8000/api/v1/birthing-person/register',
      { method: 'POST', headers: headers }
    );
    if (response.ok) {
      const data: BirthingPersonResponse = await response.json()
      return data.birthing_person
    } else {
      return null
    }
  }

  const fetchBirthingPerson = async (): Promise<BirthingPersonDTO | null> => {
    const response = await fetch(
      'http://localhost:8000/api/v1/birthing-person/',
      { method: 'GET', headers: headers }
    );
    if (response.ok) {
      const data: BirthingPersonResponse = await response.json()
      return data.birthing_person
    } else {
      return null
    }
  }

  const fetchSubscriptions = async (): Promise<BirthingPersonSummaryDTO[] | null> => {
    const response = await fetch(
      'http://localhost:8000/api/v1/subscriber/subscriptions',
      { method: 'GET', headers: headers }
    );
    if (response.ok) {
      const data: GetSubscriptionsResponse = await response.json()
      return data.subscriptions
    } else {
      return null
    }
  }

  useEffect(() => {
    const fetchData = async () => {
      let birthingPersonResponse = await fetchBirthingPerson()
      if (birthingPersonResponse === null) {
        birthingPersonResponse = await registerBirthingPerson()
        setNewUser(true);
      }
      if (birthingPersonResponse === null) {
        setError("Failed to fetch birthing person data. Please try again later.")
        setIsLoading(false);
      } else {
        setBirthingPerson(birthingPersonResponse)
      }

      let subscriptionsResponse = await fetchSubscriptions()
      if (subscriptionsResponse === null) {
        setPromptForSubscriberRegistration(true)
      } else {
        setSubscriptions(subscriptionsResponse)
      }
      setIsLoading(false);
    }
    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div>
        <Header active={page} />
        <PageLoading />
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <Header active={page} />
        <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
          <div className="text-xl text-red-600">{error}</div>
        </div>
      </div>
    );
  }

  if (promptForSubscriberRegistration) {
    return (
      <ContactMethodsModal name={birthingPerson?.first_name || ""} promptForContactMethods={setPromptForSubscriberRegistration}/>
    )
  }

  const subscriptionsProps = {
    subscriptions: subscriptions ? subscriptions : []
  }
  return (
    <div>
      <Header active={page} />
      <Container size={1200} p={15}>
        <div></div>
        <Title>Welcome {!newUser && 'back'} {auth.user?.profile.given_name}</Title>
        <Space h="xl" />
        {birthingPerson && <Labours birthingPerson={birthingPerson} />}
        <Space h="xl" />
        <Subscriptions {...subscriptionsProps} />
      </Container>
    </div>
  );
};
