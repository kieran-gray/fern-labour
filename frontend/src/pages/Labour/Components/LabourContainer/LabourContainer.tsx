import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Space, Text, Title } from '@mantine/core';
import { ApiError, LabourService, OpenAPI } from '../../../../client';
import { NotFoundError } from '../../../../Errors.tsx';
import { ErrorContainer } from '../../../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { LabourStatistics } from '../../../../shared-components/LabourStatistics/LabourStatistics.tsx';
import { PageLoading } from '../../../../shared-components/PageLoading/PageLoading.tsx';
import BeginLabourButton from '../Buttons/BeginLabour';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import { LabourControls } from '../LabourControls/LabourControls.tsx';
import { LabourUpdates } from '../LabourUpdates/LabourUpdates.tsx';
import { Contractions } from './Contractions.tsx';

export default function LabourContainer() {
  const auth = useAuth();

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['labour', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await LabourService.getActiveLabourApiV1LabourActiveGet();
        return response.labour;
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) {
          throw new NotFoundError();
        }
        throw new Error('Failed to load labour. Please try again later.');
      }
    },
    retry: 0,
  });

  if (isPending) {
    return (
      <div>
        <PageLoading />
      </div>
    );
  }

  if (isError) {
    if (error instanceof NotFoundError) {
      return (
        <div className={baseClasses.flexColumn} style={{ maxWidth: '1100px', flexGrow: 1 }}>
          <LabourControls activeContraction={false} />
          <div className={baseClasses.root}>
            <div className={baseClasses.header}>
              <Title fz="xl" className={baseClasses.title}>
                Begin Labour
              </Title>
            </div>
            <div className={baseClasses.body}>
              <Text className={baseClasses.text}>You're not currently in active labour.</Text>
              <Text className={baseClasses.text}>Click the button below to begin</Text>
              <Space h="xl" />
              <div className={baseClasses.flexRowEndNoBP} style={{ alignItems: 'stretch' }}>
                <BeginLabourButton />
              </div>
            </div>
          </div>
        </div>
      );
    }
    return <ErrorContainer message={error.message} />;
  }

  const labour = data;
  const activeContraction = labour.contractions.find((contraction) => contraction.is_active);

  return (
    <div className={baseClasses.flexColumn} style={{ maxWidth: '1100px', flexGrow: 1 }}>
      <LabourControls activeContraction={!!activeContraction} />
      <Space h="xl" />
      <Contractions labour={labour} />
      <Space h="xl" />
      <LabourStatistics labour={labour} completed={false} />
      <Space h="xl" />
      <LabourUpdates announcementHistory={labour.announcements} />
    </div>
  );
}
