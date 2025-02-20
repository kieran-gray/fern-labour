import { useRef } from 'react';
import { Space, Stack, Text, Title } from '@mantine/core';
import { LabourDTO } from '../../../../client/index.ts';
import { ContainerHeader } from '../../../../shared-components/ContainerHeader/ContainerHeader.tsx';
import { sortContractions } from '../../../../shared-components/utils.tsx';
import { ActiveContractionControls } from './ActiveContractionControls.tsx';
import { CallMidwifeAlert } from './Alerts/CallMidwifeAlert.tsx';
import { GoToHospitalAlert } from './Alerts/GoToHospitalAlert.tsx';
import ContractionTimeline from './ContractionTimeline.tsx';
import StartContractionButton from './StartContractionButton.tsx';
import { StopwatchHandle } from './Stopwatch/Stopwatch.tsx';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './Contractions.module.css';

export function Contractions({ labour }: { labour: LabourDTO }) {
  const stopwatchRef = useRef<StopwatchHandle>(null);

  const sortedContractions = sortContractions(labour.contractions);
  const activeContraction = labour.contractions.find((contraction) => contraction.is_active);

  return (
    <div className={baseClasses.root}>
      <ContainerHeader title="Contractions" />
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title order={3}>Track your contractions</Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              Track your contractions here. Simply press the button below to start a new
              contraction. Click on a completed contraction to edit it.
            </Text>
            <Stack align="stretch" justify="flex-end" mt="20px">
              {(sortedContractions.length > 0 && (
                <ContractionTimeline contractions={sortedContractions} />
              )) || (
                <Text c="var(--mantine-color-gray-9)" fw={500} mb={30}>
                  When you start your first contraction, we will let your subscribers know that your
                  labour is starting.
                </Text>
              )}
            </Stack>
            <div className={baseClasses.flexColumnEnd}>
              {sortedContractions.length > 0 && <Space h="xl" />}
              <Stack align="stretch" justify="flex-end">
                {labour.should_call_midwife_urgently && <CallMidwifeAlert />}
                {labour.should_go_to_hospital && <GoToHospitalAlert />}
                {activeContraction && (
                  <ActiveContractionControls
                    stopwatchRef={stopwatchRef}
                    activeContraction={activeContraction}
                  />
                )}
                {!activeContraction && <StartContractionButton stopwatchRef={stopwatchRef} />}
              </Stack>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
