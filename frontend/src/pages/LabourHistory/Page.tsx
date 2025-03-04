import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Space } from '@mantine/core';
import { LabourService, OpenAPI } from '../../client/index.ts';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading.tsx';
import Plan from '../Labour/Tabs/Manage/Plan/Plan.tsx';
import { LabourHistory } from './Components/LabourHistory/LabourHistory.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';

export const LabourHistoryPage = () => {
  const auth = useAuth();
  const navigate = useNavigate();

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['labours', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await LabourService.getAllLaboursApiV1LabourGetAllGet();
        return response.labours;
      } catch (err) {
        throw new Error('Failed to load labours. Please try again later.');
      }
    },
  });

  if (isPending) {
    return <PageLoading />;
  }

  if (isError) {
    return <ErrorContainer message={error.message} />;
  }

  return (
    <div className={baseClasses.flexPageColumn}>
      <Plan
        labour={undefined}
        setActiveTab={() => {
          navigate('/');
        }}
      />
      {data.length > 0 && <Space h="xl" />}
      {data.length > 0 && <LabourHistory />}
    </div>
  );
};
