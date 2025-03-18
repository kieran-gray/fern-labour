import { PageContainerContentBottom } from '../../../../../shared-components/PageContainer/PageContainer';
import image from '../../../../Subscribe/Components/protected.svg';
import { SubscribersTable } from './SubscribersTable/SubscribersTable';

export function SubscribersContainer() {
  return (
    <PageContainerContentBottom
      title="Manage your subscribers"
      description="Here, you can view and manage your subscribers. Stay in control of who can view your labour by removing or blocking unwanted subscribers."
      image={image}
      mobileImage={image}
      mobileTitle="Manage your subscribers"
    >
      <SubscribersTable />
    </PageContainerContentBottom>
  );
}
