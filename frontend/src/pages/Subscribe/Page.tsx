import { Header } from "../../shared-components/Header/Header";
import { Container, Notification, Space } from "@mantine/core";
import SubscribeForm from "./Components/Form";
import { useParams } from "react-router-dom";
import { useAuth } from "react-oidc-context";
import { BirthingPersonSummaryDTO, OpenAPI, SubscriberService } from "../../client";
import { useEffect, useState } from "react";

export const SubscribePage: React.FC = () => {
    const [newUser, setNewUser] = useState<boolean>(false);
    const [error, setError] = useState<string>("")
    const auth = useAuth();
    const { id } = useParams<'id'>();
    if (!id) throw new Error('id is required')
    OpenAPI.TOKEN = async () => {
            return auth.user?.access_token || ""
        }

    const fetchSubscriptions = async (): Promise<BirthingPersonSummaryDTO[] | null> => {
        try {
            const response = await SubscriberService.getSubscriptionsApiV1SubscriberSubscriptionsGet()
            return response.subscriptions
        } catch (err) {
            return null
        }
    }

    useEffect(() => {
        const fetchData = async () => {
          let subscriptionsResponse = await fetchSubscriptions()
          if (subscriptionsResponse === null) {
            setNewUser(true)
          }
        }
        fetchData();
      }, []);

    return (
        <div>
            <Header active="" />
            <Container size={800} p={15}>
                {error &&
                <>
                    <Notification color="red" radius="md" title="Error" onClose={() => setError("")}>
                        Invalid or incorrect token
                    </Notification>
                    <Space h="xl"></Space>
                </>
                }
                <SubscribeForm birthingPersonId={id} newUser={newUser} setNewUser={setNewUser} setError={setError} />
            </Container>
        </div>
    );
}