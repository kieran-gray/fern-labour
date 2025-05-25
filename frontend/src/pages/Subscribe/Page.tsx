import { AppShell } from '@shared/AppShell';
import { useParams, useSearchParams } from 'react-router-dom';
import SubscribeForm from './Components/Form';
import baseClasses from '@shared/shared-styles.module.css';

export const SubscribePage: React.FC = () => {
  const { id } = useParams<'id'>();
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  if (!id) {
    throw new Error('id is required');
  }

  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <SubscribeForm labourId={id} token={token} />
      </div>
    </AppShell>
  );
};
