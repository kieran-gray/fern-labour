import { Image, Text } from '@mantine/core';
import { ResponsiveTitle } from '../ResponsiveTitle/ResponsiveTitle';
import baseClasses from '../shared-styles.module.css';
import classes from './PageContainer.module.css';

interface PageContainerProps {
  title: string;
  description: string;
  image?: string;
  mobileImage?: string;
  children: React.ReactNode;
  mobileTitle?: string;
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
        <div className={classes.inner}>
          <div className={classes.content}>
            <ResponsiveTitle title={title} />
            <Text c="var(--mantine-color-gray-7)" mt="md">
              {description}
            </Text>
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
        <div className={classes.inner} style={{ paddingTop: 0 }}>
          {children}
        </div>
      </div>
    </div>
  );
}
