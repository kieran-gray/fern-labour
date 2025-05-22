import { Image } from '@mantine/core';
import { ResponsiveDescription } from '../../../../shared-components/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '../../../../shared-components/ResponsiveTitle/ResponsiveTitle';
import image from '../../../Subscriptions/Components/ManageSubscriptions/image.svg';
import { LabourHistoryTable } from './LabourHistoryTable/LabourHistoryTable';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './LabourHistory.module.css';

export function LabourHistory() {
  const title = 'Your labour history';
  const description =
    "Here you can explore your complete labour history. Each entry captures the details of your experience, from first contraction to your baby's arrival. Select any record to view the full timeline and statistics.";
  return (
    <div className={baseClasses.root} style={{ width: '100%', flexGrow: 1 }}>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <ResponsiveTitle title={title} />
            <ResponsiveDescription description={description} marginTop={10} />
            <div className={classes.imageFlexRow}>
              <Image src={image} className={classes.smallImage} />
            </div>
          </div>
          <Image src={image} className={classes.image} />
        </div>

        <div className={classes.inner} style={{ paddingTop: '0' }}>
          <LabourHistoryTable />
        </div>
      </div>
    </div>
  );
}
