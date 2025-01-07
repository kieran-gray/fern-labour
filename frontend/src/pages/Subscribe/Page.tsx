import { Header } from "../../shared-components/Header/Header";
import { Container, Notification, Space } from "@mantine/core";
import SubscribeForm from "./Components/Form";
import { useParams } from "react-router-dom";
import { useAuth } from "react-oidc-context";
import { ApiError, OpenAPI, SubscriberService } from "../../client";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { NotFoundError } from "../../Errors";

export const SubscribePage: React.FC = () => {
    const [newUser, setNewUser] = useState<boolean>(false);
    const [err, setErr] = useState<string>("")
    const auth = useAuth();
    const { id } = useParams<'id'>();
    if (!id) throw new Error('id is required')
    OpenAPI.TOKEN = async () => {
            return auth.user?.access_token || ""
        }

    useQuery({
        queryKey: ['subscriber', auth.user?.profile.sub],
        queryFn: async () => {
            try {
                const response = await SubscriberService.getApiV1SubscriberGet();
                return response.subscriber;
            } catch (err) {
                if (err instanceof ApiError && err.status === 404) {
                    setNewUser(true)
                    throw new NotFoundError();
                }
                throw new Error("Failed to load subscriber. Please try again later.")
            }
        },
        retry: (failureCount, error) => {
            if (error instanceof NotFoundError) {
                setNewUser(true)
                return false;
            }
            return failureCount < 3;
        },
    });

    return (
        <div>
            <Header active="" />
            <Container size={800} p={15}>
                {err &&
                <>
                    <Notification color="red" radius="md" title="Error" onClose={() => setErr("")}>
                        Invalid or incorrect token
                    </Notification>
                    <Space h="xl"></Space>
                </>
                }
                <SubscribeForm birthingPersonId={id} newUser={newUser} setNewUser={setNewUser} setError={setErr} />
            </Container>
        </div>
    );
}