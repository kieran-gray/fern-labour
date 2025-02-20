import { useParams, useSearchParams } from 'react-router-dom';
import { Center } from '@mantine/core';
import { Header } from '../../shared-components/Header/Header';
import SubscribeForm from './Components/Form';

export const SubscribePage: React.FC = () => {
  const { id } = useParams<'id'>();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  if (!id) {
    throw new Error('id is required');
  }

  return (
    <div>
      <Header />
      <Center flex="shrink" p={15}>
        <SubscribeForm labourId={id} token={token} />
      </Center>
    </div>
  );
};
