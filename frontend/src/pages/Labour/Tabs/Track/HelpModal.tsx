import { Anchor, Modal, Text, Title } from '@mantine/core';
import { CallMidwifeAlert } from './Alerts/CallMidwifeAlert';
import { GoToHospitalAlert } from './Alerts/GoToHospitalAlert';
import { PrepareForHospitalAlert } from './Alerts/PrepareForHospital';
import modalClasses from '../../../../shared-components/Modal.module.css';
import baseClasses from '../../../../shared-components/shared-styles.module.css';

type CloseFunctionType = (...args: any[]) => void;

export const ContractionsHelpModal = ({
  opened,
  close,
}: {
  opened: boolean;
  close: CloseFunctionType;
}) => {
  return (
    <Modal
      opened={opened}
      onClose={close}
      title="Help"
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
        style={{ flexDirection: 'column', paddingLeft: '5px', paddingRight: '5px' }}
      >
        <Title order={3} visibleFrom="md">
          Tracking your contractions
        </Title>
        <Title order={4} mt="xs" hiddenFrom="md">
          Tracking your contractions
        </Title>
        <Text mt={10} size="sm" c="var(--mantine-color-gray-8)">
          At the beginning of your contraction tap 'Start Contraction' and at the end tap 'End
          Contraction'.
          <br />
          <br />
          While your contraction is being timed you will have access to a slider to set the
          intensity.
          <br />
          Don't worry if you don't set it, you can always set it later by editing the contraction.
          <br />
          <br />
          To edit a contraction, simply tap on it and a popup will open. Here you can edit the start
          time, end time, and intensity of the contraction.
          <br />
          You can also delete a contraction through the same popup.
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
          Additionally, the contraction intensity is shown as a number inside each contraction.
        </Text>
        <Title order={3} mt="lg" visibleFrom="md">
          When to contact a midwife
        </Title>
        <Title order={4} mt="lg" hiddenFrom="md">
          When to contact a midwife
        </Title>
        <Text mt={10} size="sm" c="var(--mantine-color-gray-8)">
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
        </Text>
        <Title order={3} mt="lg" visibleFrom="md">
          When to go to the hospital
        </Title>
        <Title order={4} mt="lg" hiddenFrom="md">
          When to go to the hospital
        </Title>
        <Text mt={10} size="sm" c="var(--mantine-color-gray-8)">
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
          <br />
          <Anchor
            href="https://www.nhs.uk/pregnancy/labour-and-birth/what-happens/the-stages-of-labour-and-birth/"
            target="_blank"
          >
            For more info see this NHS page.
          </Anchor>
        </Text>
      </div>
    </Modal>
  );
};
