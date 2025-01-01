import { Header } from "../components/Header/Header";
import { Container } from "@mantine/core";
import SubscribeForm from "../components/SubscribeForm/SubscribeForm";
import { useParams } from "react-router-dom";

export const SubscribePage: React.FC = () => {
    const { id } = useParams<'id'>();
    if (!id) throw new Error('id is required')


    return (
        <div>
            <Header active="" />
            <Container size={800} p={0}>
                <SubscribeForm birthingPersonId={id} />
            </Container>
        </div>
    );
}