import { useEffect, useState } from "react";
import { BirthingPersonSummaryDTO, SubscriberDTO, BirthingPersonResponse, BirthingPersonDTO, SubscriberResponse, GetSubscriptionsResponse } from "../client";
import { Header } from "../components/Header/Header";
import { useAuth } from "react-oidc-context";
import SubscriptionsContainer from "../components/SubscriptionsContainer/SubscriptionsContainer";
import { PageLoading } from "../components/PageLoading/PageLoading";
import { Container, Space, Title } from "@mantine/core";
import BirthingPersonContainer from "../components/BirthingPersonContainer/BirthingPersonContainer";

export const HomePage: React.FC = () => {
  const [birthingPerson, setBirthingPerson] = useState<BirthingPersonDTO | null>(null);
  const [subscriptions, setSubscriptions] = useState<BirthingPersonSummaryDTO[]>([]);
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

  const registerSubscriber = async (): Promise<SubscriberDTO | null> => {
    const headers = {
      'Authorization': `Bearer ${auth.user?.access_token}`,
      'Content-Type': 'application/json'
    }
    const response = await fetch(
      'http://localhost:8000/api/v1/subscriber/register',
      { method: 'POST', headers: headers, body: JSON.stringify({"contact_methods": []})}
    );
    if (response.ok) {
      const data: SubscriberResponse = await response.json()
      return data.subscriber
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
        const subscriberResponse = await registerSubscriber()
        if (subscriberResponse === null) {
          setError("Failed to register subscriber. Please try again later.")
          setIsLoading(false);
        }
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

  const subscriptionsProps = {
    subscriptions: subscriptions ? subscriptions : []
  }
  const birthingPersonProps = {
    birthingPerson: birthingPerson
  }

  return (
    <div>
      <Header active={page} />
      <Container size={1200} p={0}>
        <Title>Welcome {!newUser && 'back'} {auth.user?.profile.given_name}</Title>
        <Space h="xl" />
        <BirthingPersonContainer {...birthingPersonProps} />
        <Space h="xl" />
        <SubscriptionsContainer {...subscriptionsProps} />
      </Container>
    </div>
  );
};
