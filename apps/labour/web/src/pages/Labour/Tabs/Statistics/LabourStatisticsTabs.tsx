import { ContractionReadModel, LabourReadModel } from '@base/clients/labour_service_v2';
import { Space, Tabs } from '@mantine/core';
import { filterContractions, LabourStatistics } from './LabourStatistics';
import { LabourStatisticsChart } from './LabourStatisticsChart';
import { LabourStatisticsTable } from './LabourStatsticsTable';
import classes from './LabourStatistics.module.css';

export const LabourStatisticsTabs = ({
  labour,
  contractions,
  statistics,
}: {
  labour: LabourReadModel;
  contractions: ContractionReadModel[];
  statistics: LabourStatistics;
}) => {
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
            <Space h="lg" />
            <LabourStatisticsChart
              contractions={contractions}
              endTime={labour.end_time ? new Date(labour.end_time) : undefined}
            />
          </Tabs.Panel>
        )}
        {statistics.last_60_mins && (
          <Tabs.Panel value="60mins">
            <LabourStatisticsTable data={statistics.last_60_mins} />
            <Space h="lg" />
            <LabourStatisticsChart
              minutes={60}
              contractions={filterContractions(contractions, 60)}
            />
          </Tabs.Panel>
        )}
        {statistics.last_30_mins && (
          <Tabs.Panel value="30mins">
            <LabourStatisticsTable data={statistics.last_30_mins} />
            <Space h="lg" />
            <LabourStatisticsChart
              minutes={30}
              contractions={filterContractions(contractions, 30)}
            />
          </Tabs.Panel>
        )}
      </Tabs.List>
    </Tabs>
  );
};
