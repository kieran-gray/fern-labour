import { Tabs, Text } from '@mantine/core';
import { LabourStatisticsDTO } from '../../client';
import { LabourStatisticsTable } from './LabourStatsticsTable';
import classes from './LabourStatistics.module.css';

export const LabourStatisticsTabs = ({ statistics }: { statistics: LabourStatisticsDTO }) => {
  return (
    <Tabs
      variant="pills"
      defaultValue="all"
      orientation="horizontal"
      classNames={{
        root: classes.labourStatsTabsRoot,
        panel: classes.labourStatsTabsPanel,
        tab: classes.labourStatsTabsTab,
      }}
    >
      <Tabs.List justify="space-between" style={{ width: '100%' }}>
        {statistics.total && <Tabs.Tab value="all">All</Tabs.Tab>}
        {statistics.last_60_mins && <Tabs.Tab value="60mins">Past 60 Mins</Tabs.Tab>}
        {statistics.last_30_mins && <Tabs.Tab value="30mins">Past 30 Mins</Tabs.Tab>}
        {statistics.total && (
          <Tabs.Panel value="all">
            <LabourStatisticsTable data={statistics.total} />
          </Tabs.Panel>
        )}
        <Tabs.Panel value="60mins">
          {(statistics.last_60_mins && (
            <LabourStatisticsTable data={statistics.last_60_mins} />
          )) || <Text className={classes.labourStatsText}>No data from the past 60 minutes</Text>}
        </Tabs.Panel>
        <Tabs.Panel value="30mins">
          {(statistics.last_30_mins && (
            <LabourStatisticsTable data={statistics.last_30_mins} />
          )) || <Text className={classes.labourStatsText}>No data from the past 30 minutes</Text>}
        </Tabs.Panel>
      </Tabs.List>
    </Tabs>
  );
};
