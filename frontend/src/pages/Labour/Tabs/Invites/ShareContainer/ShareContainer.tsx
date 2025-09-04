import { useLabour } from '@labour/LabourContext';
import { useSubscriptionToken } from '@shared/hooks';
import { PageLoadingIcon } from '@shared/PageLoading/Loading';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { Group, Image, Space, Text, Title } from '@mantine/core';
import { CopyButton } from '../CopyButton/CopyButton';
import QRButton from '../QRButton/QRButton';
import image from './share.svg';
import classes from './ShareContainer.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export function ShareContainer() {
  const { labourId } = useLabour();
  const { isPending, isError, data, error } = useSubscriptionToken();

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

  const title = 'Share with your circle';
  const description =
    'Share your labour updates with friends and family who want to be part of your journey.';
  const shareUrl = `${window.location.origin}/subscribe/${labourId}`;
  const shareText = `Hey! I'd love for you to be part of my labour circle.\nUse the link below to sign up and get updates as things happen:\n\n${shareUrl}\n\nYou'll need this code for access: ${data}`;

  return (
    <div className={baseClasses.inner}>
      <div className={classes.content}>
        <ResponsiveTitle title={title} />
        <ResponsiveDescription description={description} marginTop={10} />
        <div className={classes.imageFlexRow} style={{ marginTop: '20px' }}>
          <Image src={image} className={classes.smallImage} />
        </div>
        <Group mt={30}>
          <div className={classes.flexRow}>
            <CopyButton
              text={shareText}
              shareData={{
                title: 'Join My Labour Circle',
                url: shareUrl,
              }}
            />
            <Space w="sm" />
            <QRButton url={`${shareUrl}?token=${data}`} />
          </div>
        </Group>
      </div>
      <Image src={image} className={classes.image} />
    </div>
  );
}
