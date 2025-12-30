import { ResponsiveDescription } from '@components/ResponsiveDescription';
import { ResponsiveTitle } from '@components/ResponsiveTitle';
import { Image } from '@mantine/core';
import baseClasses from '../shared-styles.module.css';
import classes from './PageContainer.module.css';

interface PageContainerProps {
  title: string;
  description: string;
  image?: string;
  mobileImage?: string;
  children?: React.ReactNode;
}

export function PageContainerContentBottom({
  title,
  description,
  image,
  mobileImage,
  children,
}: PageContainerProps) {
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <div className={classes.content}>
            <ResponsiveTitle title={title} />
            <ResponsiveDescription description={description} marginTop={10} />
            {mobileImage && (
              <div className={classes.imageFlexRow}>
                <Image src={mobileImage} className={classes.mobileImage} />
              </div>
            )}
          </div>
          {image && (
            <div className={baseClasses.flexColumn}>
              <Image src={image} className={classes.image} />
            </div>
          )}
        </div>
        <div className={baseClasses.inner} style={{ paddingTop: 0, paddingBottom: 0 }}>
          {children}
        </div>
      </div>
    </div>
  );
}
