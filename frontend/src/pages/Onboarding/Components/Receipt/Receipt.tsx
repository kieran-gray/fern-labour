import { Image, Text, Title } from '@mantine/core';
import image from './thanks.svg';
import classes from './Receipt.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export const RecieptContainer = () => {
  return (
    <div className={baseClasses.flexColumn} style={{ width: '100%', position: 'relative' }}>
      <div className={baseClasses.inner} style={{ padding: 0 }}>
        <div className={baseClasses.content}>
          <Title order={2}>Your Journey Begins!</Title>
          <Text c="var(--mantine-color-gray-7)" mt="md">
            Payment confirmed. Thank you for choosing fernlabour.com.
            <br />
            <br />
            Your birth story deserves to be shared with those who matter most. We're honoured to
            help you connect with your loved ones during this special time.
            <br />
            <br />
            Need help? Our support team is ready to assist at support@fernlabour.com.
          </Text>
          <div className={baseClasses.imageFlexRow}>
            <Image src={image} className={classes.smallImage} />
          </div>
        </div>
        <div className={baseClasses.flexColumn}>
          <Image src={image} className={classes.image} />
        </div>
      </div>
    </div>
  );
};
