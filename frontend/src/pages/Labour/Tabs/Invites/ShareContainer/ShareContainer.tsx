import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Group, Image, Space, Text, Title } from '@mantine/core';
import { LabourService, OpenAPI } from '../../../../../clients/labour_service';
import { PageLoadingIcon } from '../../../../../shared-components/PageLoading/Loading';
import { useLabour } from '../../../LabourContext';
import { CopyButton } from '../CopyButton/CopyButton';
import QRButton from '../QRButton/QRButton';
import image from './share.svg';
import classes from './ShareContainer.module.css';

export function ShareContainer() {
  const auth = useAuth();
  const { labourId } = useLabour();
  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['token', auth.user?.profile.sub],
    queryFn: async () => {
      const response = await LabourService.getSubscriptionToken();
      return response.token;
    },
  });

  if (isPending) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <PageLoadingIcon />
      </div>
    );
  }

  if (isError) {
    return (
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Title order={3}>Error :(</Title>
        <Text>{error.message}</Text>
      </div>
    );
  }

  // TODO environment variable for frontend host
  const shareUrl = `https://track.fernlabour.com/subscribe/${labourId}`;
  const shareText = `Hey, follow this link and sign up to get notifications about my labour:\n\n${shareUrl}\n\nYou'll also need this code: ${data}`;
  return (
    <div className={classes.inner}>
      <div className={classes.content}>
        <Title order={2} visibleFrom="sm">
          Or share this link
        </Title>
        <Title order={3} hiddenFrom="sm">
          Or share this link
        </Title>
        <Text c="var(--mantine-color-gray-7)" mt="md">
          Share this link with your friends and family, make sure to include the code at the bottom
          of the message.
        </Text>
        <div className={classes.imageFlexRow} style={{ marginTop: '20px' }}>
          <Image src={image} className={classes.smallImage} />
        </div>
        <Group mt={30}>
          <div className={classes.share}>
            <Text fw={500} fz="md" mb={20}>
              Hey, follow this link and sign up to get notifications about my labour:
            </Text>
            <Text
              fw={500}
              fz="md"
              mb={25}
              style={{ overflowWrap: 'break-word', wordBreak: 'break-all' }}
            >
              {shareUrl}
            </Text>
            <Text fz="sm">
              You'll also need this code: <strong>{data}</strong>
            </Text>
          </div>
          <div className={classes.flexRow}>
            <CopyButton text={shareText} />
            <Space w="sm" />
            <QRButton url={`${shareUrl}?token=${data}`} />
          </div>
        </Group>
      </div>
      <Image src={image} className={classes.image} />
    </div>
  );
}
