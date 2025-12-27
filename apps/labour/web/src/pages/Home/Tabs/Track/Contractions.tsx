import { useEffect } from 'react';
import { LabourReadModel, SubscriberRole } from '@base/clients/labour_service/types';
import { useContractionsV2, useLabourV2Client } from '@base/hooks';
import { ImportantText } from '@shared/ImportantText/ImportantText';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { IconBook } from '@tabler/icons-react';
import { ActionIcon, Image, Stack } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { AlertContainer } from './Alerts';
import { ContractionControls } from './ContractionControls';
import ContractionTimelineCustom from './ContractionTimelineCustom';
import { ContractionsHelpModal } from './HelpModal';
import image from './Track.svg';
import classes from './Contractions.module.css';
import baseClasses from '@shared/shared-styles.module.css';

interface ContractionsProps {
  labour: LabourReadModel;
  isSubscriberView?: boolean;
  subscriberRole?: SubscriberRole;
}

const MESSAGES = {
  OWNER_TITLE: 'Track your contractions',
  OWNER_DESCRIPTION_ACTIVE:
    'Track your contractions here. Simply press the button below to start a new contraction. Click the book icon above for more info.',
  OWNER_DESCRIPTION_COMPLETED:
    "Here's a record of your contractions during labour. All contraction data is preserved for your reference.",
  OWNER_EMPTY_STATE: "You haven't logged any contractions yet",
  BIRTH_PARTNER_TITLE: (firstName: string) => `Track ${firstName}'s contractions`,
  BIRTH_PARTNER_DESCRIPTION_ACTIVE: (firstName: string) =>
    `Track ${firstName}'s contractions here. Simply press the button below to start a new contraction. Click the book icon above for more info.`,
  BIRTH_PARTNER_DESCRIPTION_COMPLETED: (firstName: string) =>
    `Here's a record of ${firstName}'s contractions during labour. All contraction data is preserved for your reference.`,
  BIRTH_PARTNER_EMPTY_STATE: (firstName: string) =>
    `You haven't logged any contractions for ${firstName} yet`,
};

export function Contractions({
  labour,
  isSubscriberView = false,
  subscriberRole,
}: ContractionsProps) {
  const [opened, { open, close }] = useDisclosure(false);
  const client = useLabourV2Client();
  const { data: contractionsData } = useContractionsV2(client, labour.labour_id, 20);

  const isBirthPartner = isSubscriberView && subscriberRole === SubscriberRole.BIRTH_PARTNER;
  const motherFirstName = labour.mother_name.split(' ')[0];

  const contractions = contractionsData?.data || [];

  const sortedContractions = [...contractions].sort((a, b) => {
    return new Date(a.duration.start_time).getTime() - new Date(b.duration.start_time).getTime();
  });

  useEffect(() => {
    const main = document.getElementById('app-main');
    if (main) {
      main.scrollTo({ top: main.scrollHeight, behavior: 'smooth' });
    }
  }, [labour]);

  const completed = labour.end_time !== null;
  const activeContraction = contractions.find(
    (contraction) => contraction.duration.start_time === contraction.duration.end_time
  );

  const title = isBirthPartner
    ? MESSAGES.BIRTH_PARTNER_TITLE(motherFirstName)
    : MESSAGES.OWNER_TITLE;

  const activeDescription = isBirthPartner
    ? MESSAGES.BIRTH_PARTNER_DESCRIPTION_ACTIVE(motherFirstName)
    : MESSAGES.OWNER_DESCRIPTION_ACTIVE;

  const completedDescription = isBirthPartner
    ? MESSAGES.BIRTH_PARTNER_DESCRIPTION_COMPLETED(motherFirstName)
    : MESSAGES.OWNER_DESCRIPTION_COMPLETED;

  const emptyStateMessage = isBirthPartner
    ? MESSAGES.BIRTH_PARTNER_EMPTY_STATE(motherFirstName)
    : MESSAGES.OWNER_EMPTY_STATE;

  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={classes.titleRow}>
          <div className={classes.title} style={{ paddingBottom: 0 }}>
            <ResponsiveTitle title={title} />
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
                  <ImportantText message={emptyStateMessage} />
                </div>
              )}
            </Stack>
            <div className={baseClasses.flexColumnEnd}>
              <Stack align="stretch" justify="flex-end">
                <AlertContainer
                  contractions={sortedContractions}
                  firstLabour={labour.first_labour}
                />
                {/* Desktop controls - only show on larger screens */}
                <div className={classes.desktopControls}>
                  <ContractionControls
                    labourCompleted={completed}
                    activeContraction={activeContraction}
                  />
                </div>
              </Stack>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
