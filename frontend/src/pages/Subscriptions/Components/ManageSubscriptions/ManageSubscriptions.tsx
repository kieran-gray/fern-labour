import { PageContainerContentBottom } from '../../../../shared-components/PageContainer/PageContainer';
import image from './image.svg';
import { SubscriptionsTable } from './SubscriptionsTable/SubscriptionsTable';

export function SubscriptionsContainer() {
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
