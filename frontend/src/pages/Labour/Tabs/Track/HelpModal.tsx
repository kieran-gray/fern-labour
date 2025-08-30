import { ContractionDTO } from '@clients/labour_service';
import { IconHourglassHigh, IconHourglassLow } from '@tabler/icons-react';
import { Anchor, Button, Modal, Slider, Text, Title } from '@mantine/core';
import { CallMidwifeAlert } from './Alerts/CallMidwifeAlert';
import { GoToHospitalAlert } from './Alerts/GoToHospitalAlert';
import { PrepareForHospitalAlert } from './Alerts/PrepareForHospital';
import ContractionTimeline from './ContractionTimeline';
import contractionClasses from './Contractions.module.css';
import modalClasses from '@shared/Modal.module.css';
import baseClasses from '@shared/shared-styles.module.css';

type CloseFunctionType = (...args: any[]) => void;

export const ContractionsHelpModal = ({
  opened,
  close,
}: {
  opened: boolean;
  close: CloseFunctionType;
}) => {
  const now = new Date();
  const mockContractions: ContractionDTO[] = [
    {
      id: 'mock-contraction-1',
      labour_id: 'mock-labour-id',
      start_time: new Date(now.getTime() - 300 * 1000).toISOString(),
      end_time: new Date(now.getTime() - 229 * 1000).toISOString(),
      duration: 71,
      intensity: 3,
      notes: null,
      is_active: false,
    },
    {
      id: 'mock-contraction-2',
      labour_id: 'mock-labour-id',
      start_time: new Date(now.getTime() - 44 * 1000).toISOString(),
      end_time: now.toISOString(),
      duration: 44,
      intensity: 2,
      notes: null,
      is_active: false,
    },
  ];
  return (
    <Modal
      opened={opened}
      onClose={close}
      title="What's this?"
      size="xl"
      transitionProps={{ transition: 'slide-left' }}
      overlayProps={{ backgroundOpacity: 0.4, blur: 3 }}
      classNames={{
        content: modalClasses.helpModalRoot,
        header: modalClasses.modalHeader,
        title: modalClasses.modalTitle,
        body: modalClasses.modalBody,
        close: modalClasses.closeButton,
      }}
    >
      <div
        className={baseClasses.inner}
        style={{
          flexDirection: 'column',
          paddingLeft: '5px',
          paddingRight: '5px',
          color: 'light-dark(var(--mantine-color-gray-9), var(--mantine-color-gray-0))',
        }}
      >
        <Title order={3} visibleFrom="md">
          Tracking your contractions
        </Title>
        <Title order={4} mt="xs" hiddenFrom="md">
          Tracking your contractions
        </Title>
        <Text
          mt={10}
          size="sm"
          c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
        >
          At the beginning of your contraction tap:
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              width: '100%',
              flexDirection: 'column',
              padding: '20px 0',
            }}
          >
            <Button
              leftSection={<IconHourglassLow size={25} />}
              radius="xl"
              size="lg"
              variant="filled"
              color="var(--mantine-primary-color-4)"
            >
              Start Contraction
            </Button>
          </div>
          At the end tap:
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              width: '100%',
              flexDirection: 'column',
              padding: '20px 0',
            }}
          >
            <Button
              leftSection={<IconHourglassHigh size={25} />}
              radius="xl"
              size="lg"
              variant="outline"
            >
              End Contraction
            </Button>
          </div>
          While your contraction is being timed you will have access to a slider to set the
          intensity:
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              width: '100%',
              flexDirection: 'column',
              padding: '20px 0',
            }}
          >
            <Text ta="center" className={baseClasses.minorText}>
              Your contraction intensity
            </Text>
            <Slider
              classNames={{
                root: contractionClasses.slider,
                markLabel: contractionClasses.markLabel,
                track: contractionClasses.track,
              }}
              color="var(--mantine-primary-color-4)"
              size="lg"
              radius="lg"
              w="60%"
              min={0}
              max={10}
              step={1}
              defaultValue={5}
              marks={[
                { value: 0, label: '0' },
                { value: 5, label: 5 },
                { value: 10, label: 10 },
              ]}
            />
          </div>
          Don't worry if you don't set it, you can always set it later by editing the contraction.
          <br />
          <br />
          On the contraction tracker screen you will see some information next to each contraction:
          <br />
          - The start time of the contraction
          <br />
          - The frequency (the time from the beginning of the previous contraction to the beginning
          of this contraction)
          <br />
          - The duration of the contraction
          <br />
          The contraction intensity is shown as a number inside each contraction.
          <div style={{ display: 'flex', justifyContent: 'center', padding: '20px 0' }}>
            <ContractionTimeline contractions={mockContractions} completed />
          </div>
        </Text>
        <Title order={3} mt="sm" visibleFrom="md">
          Editing a contraction
        </Title>
        <Title order={4} mt="sm" hiddenFrom="md">
          Editing a contraction
        </Title>
        <Text
          mt={10}
          size="sm"
          c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
        >
          To edit a contraction, simply tap on it and a popup will open. You can edit the start
          time, end time, and intensity of the contraction.
          <br />
          You can also delete a contraction through the same popup.
        </Text>
        <Title order={3} mt="xl" visibleFrom="md">
          When to go to the hospital
        </Title>
        <Title order={4} mt="xl" hiddenFrom="md">
          When to go to the hospital
        </Title>
        <Text
          mt={10}
          size="sm"
          c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
        >
          <Text fw={500} size="sm" mb={5}>
            The app will monitor your contraction pattern and alert you when:
          </Text>
          - It's time to start preparing to go to the hospital
          <br />
          <PrepareForHospitalAlert />
          <br />
          - It is time to go to the hospital
          <br />
          <GoToHospitalAlert />
          <br />
          <Text fw={500} size="sm" mb={5}>
            For first-time mothers:
          </Text>
          - You'll receive the first alert when your last 4 contractions have been 3 minutes apart
          and lasting for 1 minute.
          <br />
          - You'll receive the second alert when your contractions have matched this pattern for 1
          hour (Also known as a 3-1-1 pattern).
          <br />
          <br />
          <Text fw={500} size="sm" mb={5}>
            For those who have given birth before:
          </Text>
          - You'll receive the first alert when your last 4 contractions have been 5 minutes apart
          and lasting for 1 minute.
          <br />
          - You'll receive the second alert when your contractions have matched this pattern for 1
          hour (Also known as a 5-1-1 pattern).
          <br />
          <br />
          Keep in mind that you may not want to track continuously for over an hour, in which case
          you should consider going to the hospital when you receive the first alert.
          <br />
          <br />
          <Text fw={500}>
            Please always follow your healthcare provider's specific guidance, as they may give you
            different instructions based on your individual situation.
          </Text>
        </Text>
        <Title order={3} mt="xl" visibleFrom="md">
          When to contact a midwife
        </Title>
        <Title order={4} mt="xl" hiddenFrom="md">
          When to contact a midwife
        </Title>
        <Text
          mt={10}
          size="sm"
          c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
        >
          <Text fw={500} size="sm" mb={5}>
            Call your midwife or maternity unit for guidance if:
          </Text>
          - You think you’re in labour
          <br />
          - You’re having regular contractions coming every 5 minutes or more often
          <br />
          - You're worried about anything
          <br />
          <br />
          <Text fw={500} size="sm" mb={5}>
            Call your midwife or maternity unit urgently if:
          </Text>
          - Your waters break
          <br />
          - You have vaginal bleeding
          <br />
          - Your baby is moving less than usual
          <br />
          - You're less than 37 weeks pregnant and think you might be in labour
          <br />
          - Any of your contractions last longer than 2 minutes
          <br />
          - You're having 6 or more contractions every 10 minutes
          <br />
          The app will alert you if you should call based on the final two points above.
          <CallMidwifeAlert />
          <br />
          <Anchor
            href="https://www.nhs.uk/pregnancy/labour-and-birth/what-happens/the-stages-of-labour-and-birth/"
            target="_blank"
          >
            For additional information see this NHS page.
          </Anchor>
        </Text>
        <Text
          mt={10}
          size="sm"
          c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
        >
          Please note: Fern Labour and the materials and information it contains are not intended
          to, and do not constitute, medical or other health advice or diagnosis and should not be
          used as such. You should always consult with a qualified physician or health professional
          about your specific circumstances.
        </Text>
      </div>
    </Modal>
  );
};
