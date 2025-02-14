import { useState } from 'react';
import { Tabs} from '@mantine/core';
import { StatusUpdates } from './StatusUpdates/StatusUpdates';
import { Announcements } from './Announcements/Announcements';
import { AnnouncementDTO } from '../../../../client';

export function LabourUpdates({ announcementHistory }: { announcementHistory: AnnouncementDTO[] }) {
    const [activeTab, setActiveTab] = useState<string | null>('statusUpdates');

    return (
        <Tabs defaultValue={activeTab} value={activeTab}>
            <Tabs.Panel value="statusUpdates" pb="xs">
                <StatusUpdates setActiveTab={setActiveTab}/>
            </Tabs.Panel>
            <Tabs.Panel value="announcements" pb="xs">
                <Announcements announcementHistory={announcementHistory} setActiveTab={setActiveTab}/>
            </Tabs.Panel>
        </Tabs>
    );
}