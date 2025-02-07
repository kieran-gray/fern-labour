import { useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Badge, Button, Slider, Space, Stack, Text, Title } from '@mantine/core';
import { useInViewport, useScrollIntoView } from '@mantine/hooks';
import { ApiError, LabourService, OpenAPI } from '../../../../client';
import { NotFoundError } from '../../../../Errors.tsx';
import { ErrorContainer } from '../../../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { LabourStatistics } from '../../../../shared-components/LabourStatistics/LabourStatistics.tsx';
import { PageLoading } from '../../../../shared-components/PageLoading/PageLoading.tsx';
import {
  getTimeSinceLastStarted,
  secondsElapsed,
  sortContractions,
} from '../../../../shared-components/utils.tsx';
import { CallMidwifeAlert } from '../Alerts/CallMidwifeAlert.tsx';
import { GoToHospitalAlert } from '../Alerts/GoToHospitalAlert.tsx';
import BeginLabourButton from '../Buttons/BeginLabour';
import EndContractionButton from '../Buttons/EndContraction';
import StartContractionButton from '../Buttons/StartContraction';
import ContractionTimeline from '../ContractionTimeline/ContractionTimeline';
import Stopwatch, { StopwatchHandle } from '../Stopwatch/Stopwatch.tsx';
import { Announcements } from './Announcements.tsx';
import { CompleteLabour } from './CompleteLabour.tsx';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './LabourContainer.module.css';

export default function LabourContainer() {
  const { ref, inViewport } = useInViewport();
  const { scrollIntoView, targetRef } = useScrollIntoView<HTMLDivElement>({ offset: 60 });
  const [intensity, setIntensity] = useState(5);
  const stopwatchRef = useRef<StopwatchHandle>(null);
  const stopwatch = <Stopwatch ref={stopwatchRef} />;

  const auth = useAuth();

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['labour', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await LabourService.getActiveLabourApiV1LabourActiveGet();
        return response.labour;
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) {
          throw new NotFoundError();
        }
        throw new Error('Failed to load labour. Please try again later.');
      }
    },
    retry: 0,
  });

  if (isPending) {
    return (
      <div>
        <PageLoading />
      </div>
    );
  }

  if (isError) {
    if (error instanceof NotFoundError) {
      return (
        <div className={baseClasses.root}>
          <div className={baseClasses.header}>
            <Title fz="xl" className={baseClasses.title}>
              Begin Labour
            </Title>
          </div>
          <div className={baseClasses.body}>
            <Text className={baseClasses.text}>You're not currently in active labour.</Text>
            <Text className={baseClasses.text}>Click the button below to begin</Text>
            <Space h="xl" />
            <div className={baseClasses.flexRowEndNoBP} style={{ alignItems: 'stretch' }}>
              <BeginLabourButton />
            </div>
          </div>
        </div>
      );
    }
    return <ErrorContainer message={error.message} />;
  }

  const labour = data;

  const sortedContractions = sortContractions(labour.contractions);
  const timeSinceLastStarted = getTimeSinceLastStarted(sortedContractions);

  const activeContraction = labour.contractions.find((contraction) => contraction.is_active);
  if (activeContraction) {
    const difference = secondsElapsed(activeContraction) - (stopwatchRef.current?.seconds || 0);
    if (Math.abs(difference) > 1) {
      // We need to set the stopwatch to the current time elapsed so that on refresh
      // the stopwatch shows the correct value.
      // We should only set it if we are more than 1 second out from the contraction elapsed time.
      stopwatchRef.current?.set(secondsElapsed(activeContraction));
    }
  }

  return (
    <div className={baseClasses.flexColumn} style={{ maxWidth: '800px', flexGrow: 1 }}>
      <div className={baseClasses.root}>
        <div className={baseClasses.header}>
          <Title fz="xl" className={baseClasses.title}>
            Your Labour
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
                {activeContraction && (
                  <div className={classes.controlsBackground}>
                    {stopwatch}
                    <Space h="lg" />
                    <Text className={baseClasses.minorText}>
                      Set your contraction intensity before ending the contraction
                    </Text>
                    <Slider
                      classNames={{
                        root: classes.slider,
                        markLabel: classes.markLabel,
                        track: classes.track,
                      }}
                      color="var(--mantine-color-pink-4)"
                      size="xl"
                      radius="lg"
                      min={0}
                      max={10}
                      step={1}
                      defaultValue={5}
                      onChange={setIntensity}
                      marks={[
                        { value: 0, label: '0' },
                        { value: 5, label: 5 },
                        { value: 10, label: 10 },
                      ]}
                    />
                    <Space h="xl" />
                    <EndContractionButton intensity={intensity} stopwatchRef={stopwatchRef} />
                  </div>
                )}
                {!activeContraction && <StartContractionButton stopwatchRef={stopwatchRef} />}
              </Stack>
            </div>
          </div>
        </div>
      </div>
      <Space h="xl" />
      <LabourStatistics labour={labour} completed={false} />
      <Space h="xl" />
      <Announcements announcementHistory={labour.announcements} />
      <Space h="xl" />
      <CompleteLabour activeContraction={!!activeContraction} />
    </div>
  );
}
