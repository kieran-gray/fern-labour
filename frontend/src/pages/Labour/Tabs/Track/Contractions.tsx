import { useEffect } from 'react';
import { LabourDTO } from '@clients/labour_service/index.ts';
import { ImportantText } from '@shared/ImportantText/ImportantText.tsx';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription.tsx';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle.tsx';
import { sortContractions } from '@shared/utils.tsx';
import { IconBook } from '@tabler/icons-react';
import { ActionIcon, Image, Stack } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { CallMidwifeAlert } from './Alerts/CallMidwifeAlert.tsx';
import { GoToHospitalAlert } from './Alerts/GoToHospitalAlert.tsx';
import { PrepareForHospitalAlert } from './Alerts/PrepareForHospital.tsx';
import { ContractionControls } from './ContractionControls.tsx';
import ContractionTimelineCustom from './ContractionTimelineCustom.tsx';
import { ContractionsHelpModal } from './HelpModal.tsx';
import image from './Track.svg';
import classes from './Contractions.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export function Contractions({ labour }: { labour: LabourDTO }) {
  const [opened, { open, close }] = useDisclosure(false);

  const sortedContractions = sortContractions(labour.contractions);

  useEffect(() => {
    window.scrollTo({
      top: document.documentElement.scrollHeight,
      behavior: 'smooth',
    });
  }, [labour]);

  const completed = labour.end_time !== null;
  const activeDescription =
    'Track your contractions here. Simply press the button below to start a new contraction. Click the book icon above for more info.';
  const completedDescription =
    "Here's a record of your contractions during labour. All contraction data is preserved for your reference.";

  const alerts = !completed ? (
    <>
      {labour.recommendations.call_midwife && <CallMidwifeAlert />}
      {labour.recommendations.go_to_hospital && <GoToHospitalAlert />}
      {labour.recommendations.prepare_for_hospital && <PrepareForHospitalAlert />}
    </>
  ) : null;

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={classes.titleRow}>
          <div className={classes.title} style={{ paddingBottom: 0 }}>
            <ResponsiveTitle title="Track your contractions" />
          </div>
          <ActionIcon radius="xl" variant="light" size="xl" onClick={open}>
            <IconBook />
          </ActionIcon>
          <ContractionsHelpModal close={close} opened={opened} />
        </div>
        <div className={baseClasses.inner} style={{ paddingBottom: 0, paddingTop: 0 }}>
          <div className={classes.content}>
            <ResponsiveDescription
              description={
                completed
                  ? completedDescription
                  : sortedContractions.length === 0
                    ? activeDescription
                    : ''
              }
              marginTop={0}
            />
            <Stack align="stretch" justify="flex-end" mt="20px" style={{ alignItems: 'center' }}>
              {sortedContractions.length > 0 && (
                <ContractionTimelineCustom
                  contractions={sortedContractions}
                  completed={completed}
                />
              )}
              {sortedContractions.length === 0 && !completed && (
                <div style={{ width: '100%' }}>
                  <div className={classes.imageFlexRow}>
                    <Image src={image} className={classes.image} />
                  </div>
                  <ImportantText message="You haven't logged any contractions yet" />
                </div>
              )}
            </Stack>
            <div className={baseClasses.flexColumnEnd}>
              <Stack align="stretch" justify="flex-end">
                {alerts}
                {/* Desktop controls - only show on larger screens */}
                <div className={classes.desktopControls}>
                  <ContractionControls labour={labour} />
                </div>
              </Stack>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
