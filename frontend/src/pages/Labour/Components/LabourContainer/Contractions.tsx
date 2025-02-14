import { useRef } from 'react';
import { Badge, Button, Space, Stack, Text, Title } from '@mantine/core';
import { useInViewport, useScrollIntoView } from '@mantine/hooks';
import { LabourDTO } from '../../../../client';
import { getTimeSinceLastStarted, sortContractions } from '../../../../shared-components/utils.tsx';
import { CallMidwifeAlert } from '../Alerts/CallMidwifeAlert.tsx';
import { GoToHospitalAlert } from '../Alerts/GoToHospitalAlert.tsx';
import StartContractionButton from '../Buttons/StartContraction';
import ContractionTimeline from '../ContractionTimeline/ContractionTimeline';
import { StopwatchHandle } from '../Stopwatch/Stopwatch.tsx';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import { ActiveContractionControls } from './ActiveContractionControls.tsx';

export function Contractions({labour}: {labour: LabourDTO}) {
    const { ref, inViewport } = useInViewport();
    const { scrollIntoView, targetRef } = useScrollIntoView<HTMLDivElement>({ offset: 60 });
    const stopwatchRef = useRef<StopwatchHandle>(null);

    const sortedContractions = sortContractions(labour.contractions);
    const timeSinceLastStarted = getTimeSinceLastStarted(sortedContractions);

    const activeContraction = labour.contractions.find((contraction) => contraction.is_active);

    return (
        <div className={baseClasses.root}>
            <div className={baseClasses.header}>
                <Title fz="xl" className={baseClasses.title}>
                    Contractions
                </Title>
            </div>
            <div className={baseClasses.body}>
                <div>
                    <div className={baseClasses.flexColumn}>
                        <div className={baseClasses.flexRowEndNoBP}>
                            {!inViewport && (
                                <Button
                                    radius="lg"
                                    size="md"
                                    variant="outline"
                                    style={{ position: 'absolute' }}
                                    onClick={() => scrollIntoView({ alignment: 'center' })}
                                >
                                    ↓
                                </Button>
                            )}
                        </div>
                        <Stack align="flex-start" justify="center" gap="md" miw={200}>
                            <Badge size="xl" pl={40} pr={40} mb={20} variant="light">
                                {labour.current_phase}
                            </Badge>
                        </Stack>
                        <Stack align="stretch" justify="flex-end" h="100%">
                            <Text className={baseClasses.text}>
                                Your contractions{(sortedContractions.length > 0 && ':') || ' will appear below'}
                            </Text>
                            <ContractionTimeline
                                contractions={sortedContractions}
                                contractionGaps={timeSinceLastStarted}
                            />
                        </Stack>
                    </div>
                    <div className={baseClasses.flexColumnEnd}>
                        {sortedContractions.length > 0 && <Space h="xl" />}
                        <Stack align="stretch" justify="flex-end" h="100%">
                            {labour.should_call_midwife_urgently && <CallMidwifeAlert />}
                            {labour.should_go_to_hospital && <GoToHospitalAlert />}
                            <div ref={ref} />
                            <div ref={targetRef} />
                            {activeContraction && (<ActiveContractionControls stopwatchRef={stopwatchRef} activeContraction={activeContraction}/>)}
                            {!activeContraction && <StartContractionButton stopwatchRef={stopwatchRef} />}
                        </Stack>
                    </div>
                </div>
            </div>
        </div>
    );
}
