import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Text, Title } from '@mantine/core';
import { BirthingPersonService, OpenAPI } from '../../../../client';
import { ErrorContainer } from '../../../../shared-components/ErrorContainer/ErrorContainer';
import { PageLoading } from '../../../../shared-components/PageLoading/PageLoading';
import { CopyButton } from '../CopyButton/CopyButton';
import QRButton from '../QRButton/QRButton';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './ShareContainer.module.css';

export function ShareContainer() {
  const auth = useAuth();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };
  const userId = auth.user?.profile.sub || '';

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['token', auth.user?.profile.sub],
    queryFn: async () => {
      const response =
        await BirthingPersonService.getSubscriptionTokenApiV1BirthingPersonSubscriptionTokenGet();
      return response.token;
    },
  });

  if (isPending) {
    return <PageLoading />;
  }

  if (isError) {
    return <ErrorContainer message={error.message} />;
  }

  // TODO environment variable for frontend host
  const shareUrl = `https://track.fernlabour.com/subscribe/${userId}`;
  const shareText = `Hey, follow this link and sign up to get notifications about my labour:\n\n${shareUrl}\n\nYou'll also need this code: ${data}`;

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.header}>
        <Title fz="xl" className={baseClasses.title}>
          Share
        </Title>
      </div>
      <div className={baseClasses.body}>
        <Text className={baseClasses.text}>
          Share this link with friends and family to allow them to track your labour:
        </Text>
        <div className={classes.share}>
          <Text fw={500} fz="md" mb={5}>
            Hey, follow this link and sign up to get notifications about my labour:
            <br />
            <br />
            {shareUrl}
          </Text>
          <Text fz="sm">
            <br />
            You'll also need this code: <strong>{data}</strong>
          </Text>
        </div>
        <div className={classes.controls}>
          <div className={baseClasses.flexRow}>
            <CopyButton text={shareText} />
            <QRButton url={`${shareUrl}?token=${data}`} />
          </div>
        </div>
      </div>
    </div>
  );
}
