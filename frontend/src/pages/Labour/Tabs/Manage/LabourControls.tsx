import { useState } from 'react';
import { Tabs } from '@mantine/core';
import { LabourDTO } from '../../../../client';
import Complete from './Complete/Complete';
import LabourDetails from './LabourDetails/LabourDetails';
import Plan from './Plan/Plan';

export function LabourControls({ labour }: { labour: LabourDTO | undefined }) {
  const [activeTab, setActiveTab] = useState<string | null>('details');
  const activeContraction = labour?.contractions.find((contraction) => contraction.is_active);
  return (
    <Tabs keepMounted={false} defaultValue={activeTab} value={activeTab}>
      <Tabs.Panel value="plan" pb="xs">
        <Plan labour={labour} setActiveTab={setActiveTab} />
      </Tabs.Panel>
      <Tabs.Panel value="details" pb="xs">
        <LabourDetails setActiveTab={setActiveTab} />
      </Tabs.Panel>
      <Tabs.Panel value="complete" pb="xs">
        <Complete activeContraction={!!activeContraction} setActiveTab={setActiveTab} />
      </Tabs.Panel>
    </Tabs>
  );
}
