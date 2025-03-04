import { IconArrowLeft, IconArrowRight } from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Badge, Button, Text, Title } from '@mantine/core';
import { ApiError, LabourService, OpenAPI } from '../../../../../client';
import { NotFoundError } from '../../../../../Errors';
import { ContainerHeader } from '../../../../../shared-components/ContainerHeader/ContainerHeader';
import { PageLoadingIcon } from '../../../../../shared-components/PageLoading/Loading';
import { dueDateToGestationalAge } from '../../../../../shared-components/utils';
import { useLabour } from '../../../LabourContext';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
import classes from './LabourDetails.module.css';

export default function LabourDetails({ setActiveTab }: { setActiveTab: Function }) {
  const auth = useAuth();
  const { labourId } = useLabour();

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['labour', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await LabourService.getLabourByIdApiV1LabourGetLabourIdGet({
          labourId: labourId!,
        });
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
  let content = undefined;

  if (isPending) {
    content = (
      <div style={{ margin: 'auto' }}>
        <PageLoadingIcon />
      </div>
    );
  } else if (isError) {
    content = (
      <Text c="var(--mantine-color-gray-7)">
        Something went wrong... {error ? error.message : ''}
      </Text>
    );
  } else {
    content = (
      <div className={classes.content}>
        <Title className={classes.title}>
          {data.labour_name ? data.labour_name : 'Your Labour'}
        </Title>
        <Text c="var(--mantine-color-gray-7)" mt="md" mb="md">
          Take a deep breath—you’ve got this! Here, you can check your labour details and manage
          your subscribers. Use the tabs above to navigate through the app.
        </Text>
        <div className={classes.infoRow}>
          <Badge variant="filled" className={classes.labourBadge} size="lg">
            Not in labour
          </Badge>
          <Badge variant="filled" className={classes.labourBadge} size="lg">
            Due: {new Date(data.due_date).toLocaleDateString()}
          </Badge>
          <Badge variant="filled" className={classes.labourBadge} size="lg">
            Gestational age: {dueDateToGestationalAge(new Date(data.due_date))}
          </Badge>
          <Badge variant="filled" className={classes.labourBadge} size="lg">
            {!data.first_labour ? 'Not ' : ''}first time mother
          </Badge>
        </div>
        <div className={baseClasses.flexRow} style={{ marginTop: '20px' }}>
          <Button
            color="var(--mantine-color-pink-4)"
            leftSection={<IconArrowLeft size={18} stroke={1.5} />}
            variant="outline"
            radius="xl"
            size="md"
            h={48}
            className={classes.backButton}
            onClick={() => setActiveTab('plan')}
            type="submit"
          >
            Go back to planning
          </Button>
          <Button
            color="var(--mantine-color-pink-4)"
            rightSection={<IconArrowRight size={18} stroke={1.5} />}
            variant="filled"
            radius="xl"
            size="md"
            h={48}
            onClick={() => setActiveTab('complete')}
            type="submit"
          >
            Complete your labour
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className={baseClasses.root}>
      <ContainerHeader title="Details" />
      <div className={baseClasses.body}>
        <div className={classes.inner}>{content}</div>
      </div>
    </div>
  );
}
