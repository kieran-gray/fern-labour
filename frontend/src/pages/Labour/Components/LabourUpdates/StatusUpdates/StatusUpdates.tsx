import { Avatar, Button, Group, ScrollArea, Text, TextInput, Title, Tooltip } from '@mantine/core';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
import classes from './StatusUpdates.module.css';
import { IconPencil, IconSend, IconSwitchHorizontal } from '@tabler/icons-react';
import { useEffect, useRef, useState } from 'react';
import { useAuth } from 'react-oidc-context';

const statusUpdates = [
    {
        time: "10 minutes ago",
        update: "Contractions started this morning, they aren't really progressing so I am going to stop tracking. Will update if anything else happens."
    },
    {
        time: "1 minutes ago",
        update: "Just been to the hospital for my daily monitoring, no issues, baby is happy and healthy."
    },
    {
        time: "1 minutes ago",
        update: "Just been to the hospital for my daily monitoring, no issues, baby is happy and healthy."
    },
    {
        time: "1 minutes ago",
        update: "Just been to the hospital for my daily monitoring, no issues, baby is happy and healthy."
    },
    {
        time: "1 minutes ago",
        update: "Just been to the hospital for my daily monitoring, no issues, baby is happy and healthy."
    },
    {
        time: "1 minutes ago",
        update: "Just been to the hospital for my daily monitoring, no issues, baby is happy and healthy."
    },
    {
        time: "1 minutes ago",
        update: "Just been to the hospital for my daily monitoring, no issues, baby is happy and healthy."
    },
    {
        time: "1 minutes ago",
        update: "Just been to the hospital for my daily monitoring, no issues, baby is happy and healthy."
    },
    {
        time: "1 minutes ago",
        update: "Just been to the hospital for my daily monitoring, no issues, baby is happy and healthy."
    },
]

export function StatusUpdates({setActiveTab}: {setActiveTab: Function}) {
    const [update, setUpdate] = useState('');
    const viewport = useRef<HTMLDivElement>(null);
    const auth = useAuth();
    const userName = auth.user?.profile.name

    const statusUpdateDisplay = statusUpdates.map((data) => {
        return (
            <div className={classes.statusUpdatePanel}>
                <Group>
                    <Avatar
                        alt={userName}
                        radius="xl"
                        color="var(--mantine-color-pink-5)"
                    />
                    <div>
                        <Text size="sm" fw='700' c="var(--mantine-color-gray-9)">{userName}</Text>
                        <Text size="xs" c="var(--mantine-color-gray-9)">
                            {data.time}
                        </Text>
                    </div>
                </Group>
                <Text pl={54} pt="sm" size="sm" fw='400'>
                    {data.update}
                </Text>
            </div>
        )
    })

    const button = <Button
        color="var(--mantine-color-pink-4)"
        rightSection={<IconSend size={18} stroke={1.5} />}
        variant="filled"
        radius="xl"
        size="md"
        h={48}
        style={{ minWidth: '200px' }}
        type="submit"
        disabled={!update}
    >
        Post Update
    </Button>

    useEffect(() => {
        if (viewport.current) {
            viewport.current.scrollTo({ top: viewport.current.scrollHeight, behavior: 'auto' });
        }
    }, [statusUpdates]);

    return (
        <div className={baseClasses.root} style={{ maxWidth: '1100px' }}>
            <div className={baseClasses.header}>
                <Title fz="xl" className={baseClasses.title}>
                    Updates
                </Title>
            </div>
            <div className={baseClasses.body}>
                <div className={classes.inner}>
                    <div className={classes.content}>
                        <Title order={3}>Post a status update</Title>
                        <Text c="var(--mantine-color-gray-7)" mt="sm" mb="md">
                            Update your status here to let your subscribers know how you are getting on. They won't be notified about these updates, but they will be able to see them in the app.
                        </Text>
                        <ScrollArea.Autosize mah={400} viewportRef={viewport}>
                            <div className={classes.statusUpdateContainer}>
                                {statusUpdateDisplay}
                            </div>
                        </ScrollArea.Autosize>

                        <TextInput
                            mt={20}
                            rightSection={<IconPencil size={18} stroke={1.5} />}
                            radius="lg"
                            size="md"
                            placeholder="Your status update"
                            onChange={(event) => setUpdate(event.currentTarget.value)}
                            value={update}
                        />
                        <div className={classes.flexRow} style={{ marginTop: '10px' }}>
                            <Button
                                color="var(--mantine-color-pink-4)"
                                leftSection={<IconSwitchHorizontal size={18} stroke={1.5} />}
                                variant="outline"
                                radius="xl"
                                size="md"
                                h={48}
                                className={classes.backButton}
                                onClick={() => setActiveTab('announcements')}
                                type="submit"
                            >
                                Switch to Announcements
                            </Button>
                            {!update ? <Tooltip label="Enter a message first">{button}</Tooltip> : button}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}