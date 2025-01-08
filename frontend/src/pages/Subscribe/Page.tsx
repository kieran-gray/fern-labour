import { Header } from "../../shared-components/Header/Header";
import { Container } from "@mantine/core";
import SubscribeForm from "./Components/Form";
import { useParams } from "react-router-dom";
import { useAuth } from "react-oidc-context";
import { ApiError, OpenAPI, SubscriberService } from "../../client";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { NotFoundError } from "../../Errors";

export const SubscribePage: React.FC = () => {
    const [newUser, setNewUser] = useState<boolean>(false);
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
                <SubscribeForm birthingPersonId={id} newUser={newUser} setNewUser={setNewUser} />
            </Container>
        </div>
    );
}