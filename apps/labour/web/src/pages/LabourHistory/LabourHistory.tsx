import { ResponsiveDescription } from '@components/ResponsiveDescription';
import { ResponsiveTitle } from '@components/ResponsiveTitle';
import { LabourHistoryTable } from './LabourHistoryTable';
import classes from './LabourHistory.module.css';
import baseClasses from '@components/shared-styles.module.css';

export function LabourHistory() {
  const title = 'Your labour history';
  const description =
    'View and manage your past labour records. Select any entry to see the full timeline and statistics.';

  return (
    <div className={baseClasses.root} style={{ width: '100%', flexGrow: 1 }}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <div className={classes.header}>
            <ResponsiveTitle title={title} />
            <ResponsiveDescription description={description} marginTop={10} />
          </div>
        </div>

        <div className={baseClasses.inner} style={{ paddingTop: 0 }}>
          <LabourHistoryTable />
        </div>
      </div>
    </div>
  );
}
