import { useEffect, useRef } from 'react';
import { Space, Stack, Text, Title } from '@mantine/core';
import { useScrollIntoView } from '@mantine/hooks';
import { ContractionDTO, LabourDTO } from '../../../../client/index.ts';
import { ImportantText } from '../../../../shared-components/ImportantText/ImportantText.tsx';
import { sortContractions } from '../../../../shared-components/utils.tsx';
import { ActiveContractionControls } from './ActiveContractionControls.tsx';
import { CallMidwifeAlert } from './Alerts/CallMidwifeAlert.tsx';
import { GoToHospitalAlert } from './Alerts/GoToHospitalAlert.tsx';
import { PrepareForHospitalAlert } from './Alerts/PrepareForHospital.tsx';
import ContractionTimeline from './ContractionTimeline.tsx';
import StartContractionButton from './StartContractionButton.tsx';
import { StopwatchHandle } from './Stopwatch/Stopwatch.tsx';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './Contractions.module.css';

export function Contractions({ labour }: { labour: LabourDTO }) {
  const stopwatchRef = useRef<StopwatchHandle>(null);
  const { scrollIntoView, targetRef } = useScrollIntoView<HTMLDivElement>({
    duration: 200,
    offset: 50,
  });

  const sortedContractions = sortContractions(labour.contractions);
  const activeContraction = labour.contractions.find((contraction) => contraction.is_active);

  const anyPlaceholderContractions = (contractions: ContractionDTO[]) => {
    return contractions.some((contraction) => contraction.id === 'placeholder');
  };
  const containsPlaceholderContractions = anyPlaceholderContractions(labour.contractions);

  useEffect(() => {
    scrollIntoView({ alignment: 'end' });
  }, [labour]);

  const completed = labour.end_time !== null;
  const activeDescription =
    'Track your contractions here. Simply press the button below to start a new contraction. Click on a completed contraction to edit it.';
  const completedDescription =
    "Here's a record of your contractions during labour. All contraction data is preserved for your reference.";

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title order={2} visibleFrom="sm">
              Track your contractions
            </Title>
            <Title order={3} hiddenFrom="sm">
              Track your contractions
            </Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              {completed ? completedDescription : activeDescription}
            </Text>
            <Stack align="stretch" justify="flex-end" mt="20px" style={{ alignItems: 'center' }}>
              {sortedContractions.length > 0 && (
                <ContractionTimeline contractions={sortedContractions} completed={completed} />
              )}
              {sortedContractions.length === 0 && !completed && (
                <div style={{ width: '100%', marginBottom: '30px' }}>
                  <ImportantText message="When you start your first contraction, we will let your subscribers know that your labour is starting." />
                </div>
              )}
            </Stack>
            <div className={baseClasses.flexColumnEnd}>
              {sortedContractions.length > 0 && <Space h="xl" />}
              <Stack align="stretch" justify="flex-end">
                {labour.recommendations.call_midwife && <CallMidwifeAlert />}
                {labour.recommendations.go_to_hospital && <GoToHospitalAlert />}
                {labour.recommendations.prepare_for_hospital && <PrepareForHospitalAlert />}
                {activeContraction && (
                  <ActiveContractionControls
                    stopwatchRef={stopwatchRef}
                    activeContraction={activeContraction}
                    disabled={containsPlaceholderContractions}
                  />
                )}
                {!activeContraction && !completed && (
                  <StartContractionButton stopwatchRef={stopwatchRef} />
                )}
                <div ref={targetRef} />
              </Stack>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
