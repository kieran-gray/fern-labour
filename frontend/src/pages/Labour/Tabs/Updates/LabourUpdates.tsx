import { useState } from 'react';
import { Tabs } from '@mantine/core';
import { LabourDTO } from '../../../../client';
import { Announcements } from './Announcements/Announcements';
import { StatusUpdates } from './StatusUpdates/StatusUpdates';

export function LabourUpdates({ labour }: { labour: LabourDTO }) {
  const [activeTab, setActiveTab] = useState<string | null>('statusUpdates');
  const completed = labour.end_time != null;
  return (
    <Tabs defaultValue={activeTab} value={activeTab}>
      <Tabs.Panel value="statusUpdates" pb="xs">
        <StatusUpdates
          statusUpdates={labour.status_updates}
          setActiveTab={setActiveTab}
          completed={completed}
        />
      </Tabs.Panel>
      <Tabs.Panel value="announcements" pb="xs">
        <Announcements
          announcements={labour.announcements}
          setActiveTab={setActiveTab}
          completed={completed}
        />
      </Tabs.Panel>
    </Tabs>
  );
}
