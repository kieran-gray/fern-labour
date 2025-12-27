import image from '@base/pages/Subscribe/protected.svg';
import { PageContainerContentBottom } from '@shared/PageContainer/PageContainer';
import { ManageSubscribersTabs } from './ManageSubscriberTabs/ManageSubscriberTabs';

export function SubscribersContainer() {
  return (
    <PageContainerContentBottom
      title="Manage your subscribers"
      description="Here, you can view and manage your subscribers. Stay in control of who can view your labour by removing or blocking unwanted subscribers."
      image={image}
      mobileImage={image}
    >
      <ManageSubscribersTabs />
    </PageContainerContentBottom>
  );
}
