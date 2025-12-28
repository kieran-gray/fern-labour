import { CopyButton } from '@home/Tabs/Share/ShareLabour/CopyButton';
import image from '@home/Tabs/Share/ShareLabour/share.svg';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { Group, Image } from '@mantine/core';
import classes from '@home/Tabs/Share/ShareLabour/ShareLabour.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export function ShareFernLabour() {
  const title = 'Share Fern Labour with Others';
  const description =
    'Know someone expecting? Share FernLabour to help them keep their loved ones informed during labour.';
  const shareUrl = window.location.origin;
  const shareMessage = `Hey! I've been using FernLabour and thought you might find it useful.\n\nIt's a simple way to keep family and friends informed during labour.\n\nCheck it out:`;

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
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
                  text={shareMessage}
                  shareData={{
                    title: 'Try FernLabour',
                    url: shareUrl,
                  }}
                />
              </div>
            </Group>
          </div>
          <Image src={image} className={classes.image} />
        </div>
      </div>
    </div>
  );
}
