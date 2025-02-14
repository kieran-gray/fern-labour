import { useState } from 'react';
import { Tabs} from '@mantine/core';
import Plan from './Plan/Plan';
import Details from './Details/Details';
import Complete from './Complete/Complete';

export function LabourControls({activeContraction}: {activeContraction: boolean}) {
    const [activeTab, setActiveTab] = useState<string | null>('details');

    return (
        <Tabs defaultValue={activeTab} value={activeTab}>
            <Tabs.Panel value="plan" pb="xs">
                <Plan setActiveTab={setActiveTab} />
            </Tabs.Panel>
            <Tabs.Panel value="details" pb="xs">
                <Details setActiveTab={setActiveTab} />
            </Tabs.Panel>
            <Tabs.Panel value="complete" pb="xs">
                <Complete activeContraction={!!activeContraction} setActiveTab={setActiveTab} />
            </Tabs.Panel>
        </Tabs>
    );
}