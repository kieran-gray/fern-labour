import { useState } from 'react';
import { ContractionReadModel } from '@base/clients/labour_service';
import { Tabs } from '@mantine/core';
import Complete from './Complete/Complete';
import LabourDetails from './LabourDetails/LabourDetails';

export function ManageLabour({
  activeContraction,
}: {
  activeContraction: ContractionReadModel | undefined;
}) {
  const [activeTab, setActiveTab] = useState<string | null>('details');
  return (
    <Tabs keepMounted={false} defaultValue={activeTab} value={activeTab}>
      <Tabs.Panel value="details" pb="xs">
        <LabourDetails setActiveTab={setActiveTab} />
      </Tabs.Panel>
      <Tabs.Panel value="complete" pb="xs">
        <Complete activeContraction={activeContraction !== undefined} setActiveTab={setActiveTab} />
      </Tabs.Panel>
    </Tabs>
  );
}
