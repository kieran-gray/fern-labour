import { PageContainerContentBottom } from '@components/PageContainer/PageContainer';
import image from './subscriptions.svg';
import { SubscriptionsTable } from './SubscriptionsTable';

export function ManageSubscriptions() {
  return (
    <PageContainerContentBottom
      title="Manage your subscriptions"
      description="Here, you can view and manage the labours that you are subscribed to. Update your contact methods for each individually."
      image={image}
      mobileImage={image}
    >
      <SubscriptionsTable />
    </PageContainerContentBottom>
  );
}
