import { useEffect, useRef } from 'react';
import { IconBook } from '@tabler/icons-react';
import { ActionIcon, Image, Space, Stack } from '@mantine/core';
import { useDisclosure, useScrollIntoView } from '@mantine/hooks';
import { ContractionDTO, LabourDTO } from '../../../../clients/labour_service/index.ts';
import { ImportantText } from '../../../../shared-components/ImportantText/ImportantText.tsx';
import { ResponsiveDescription } from '../../../../shared-components/ResponsiveDescription/ResponsiveDescription.tsx';
import { ResponsiveTitle } from '../../../../shared-components/ResponsiveTitle/ResponsiveTitle.tsx';
import { sortContractions } from '../../../../shared-components/utils.tsx';
import { ActiveContractionControls } from './ActiveContractionControls.tsx';
import { CallMidwifeAlert } from './Alerts/CallMidwifeAlert.tsx';
import { GoToHospitalAlert } from './Alerts/GoToHospitalAlert.tsx';
import { PrepareForHospitalAlert } from './Alerts/PrepareForHospital.tsx';
import ContractionTimeline from './ContractionTimeline.tsx';
import { ContractionsHelpModal } from './HelpModal.tsx';
import StartContractionButton from './StartContractionButton.tsx';
import { StopwatchHandle } from './Stopwatch/Stopwatch.tsx';
import image from './Track.svg';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './Contractions.module.css';

export function Contractions({ labour }: { labour: LabourDTO }) {
  const [opened, { open, close }] = useDisclosure(false);
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
        <div className={classes.titleRow}>
          <div className={classes.title} style={{ paddingBottom: 0 }}>
            <ResponsiveTitle title="Track your contractions" />
          </div>
          <ActionIcon radius="lg" variant="light" size="xl" onClick={open}>
            <IconBook />
          </ActionIcon>
          <ContractionsHelpModal close={close} opened={opened} />
        </div>
        <div className={baseClasses.inner} style={{ paddingBottom: 0, paddingTop: 0 }}>
          <div className={classes.content}>
            <ResponsiveDescription
              description={completed ? completedDescription : activeDescription}
              marginTop={0}
            />
            <Stack align="stretch" justify="flex-end" mt="20px" style={{ alignItems: 'center' }}>
              {sortedContractions.length > 0 && (
                <ContractionTimeline contractions={sortedContractions} completed={completed} />
              )}
              {sortedContractions.length === 0 && !completed && (
                <div style={{ width: '100%', marginBottom: '25px' }}>
                  <div className={classes.imageFlexRow}>
                    <Image src={image} className={classes.image} />
                  </div>
                  <ImportantText message="You haven't logged any contractions yet" />
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
