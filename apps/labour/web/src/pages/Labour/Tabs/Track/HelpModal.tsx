import { ContractionReadModel } from '@base/clients/labour_service_v2';
import { IconHourglassHigh, IconHourglassLow } from '@tabler/icons-react';
import { Anchor, Button, List, Modal, Slider, Stack, Text, Title } from '@mantine/core';
import { CallMidwifeAlert } from './Alerts/CallMidwifeAlert';
import { GoToHospitalAlert } from './Alerts/GoToHospitalAlert';
import { PrepareForHospitalAlert } from './Alerts/PrepareForHospital';
import ContractionTimelineCustom from './ContractionTimelineCustom';
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
  const mockContractions: ContractionReadModel[] = [
    {
      contraction_id: 'mock-contraction-1',
      labour_id: 'mock-labour-id',
      duration: {
        start_time: new Date(now.getTime() - 300 * 1000).toISOString(),
        end_time: new Date(now.getTime() - 229 * 1000).toISOString(),
      },
      duration_seconds: 71,
      intensity: 3,
      created_at: now.toISOString(),
      updated_at: now.toISOString(),
    },
    {
      contraction_id: 'mock-contraction-2',
      labour_id: 'mock-labour-id',
      duration: {
        start_time: new Date(now.getTime() - 44 * 1000).toISOString(),
        end_time: now.toISOString(),
      },
      duration_seconds: 44,
      intensity: 2,
      created_at: now.toISOString(),
      updated_at: now.toISOString(),
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
        <Stack gap="xs" mt={10}>
          <Text size="sm" c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))">
            Track contractions with two quick taps:
          </Text>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              width: '100%',
              flexDirection: 'column',
            }}
          >
            <Button
              leftSection={<IconHourglassLow size={25} />}
              radius="xl"
              size="lg"
              variant="filled"
              color="var(--mantine-primary-color-4)"
              mt="xs"
            >
              Start Contraction
            </Button>
          </div>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              width: '100%',
              flexDirection: 'column',
            }}
          >
            <Button
              leftSection={<IconHourglassHigh size={25} />}
              radius="xl"
              size="lg"
              variant="outline"
              mt="xs"
            >
              End Contraction
            </Button>
          </div>
          <Text size="sm" c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))">
            While timing, you can also set the intensity:
          </Text>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              width: '100%',
              flexDirection: 'column',
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
          <Text size="sm" c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))">
            You can always adjust intensity later by editing the contraction.
          </Text>
          <Text
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
            mt="sm"
          >
            On the tracker, each contraction shows:
          </Text>
          <List
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
            withPadding
          >
            <List.Item>The start time</List.Item>
            <List.Item>
              The frequency — time from the start of the previous contraction to the start of this
              one
            </List.Item>
            <List.Item>The duration</List.Item>
            <List.Item>Intensity (shown as a number inside each contraction)</List.Item>
          </List>
          <div style={{ display: 'flex', justifyContent: 'center', padding: '12px 0 4px' }}>
            <ContractionTimelineCustom contractions={mockContractions} completed />
          </div>
        </Stack>
        <Title order={3} mt="sm" visibleFrom="md">
          Editing a contraction
        </Title>
        <Title order={4} mt="sm" hiddenFrom="md">
          Editing a contraction
        </Title>
        <Stack gap={4} mt={10}>
          <Text size="sm" c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))">
            To edit a contraction, tap it to open the editor.
          </Text>
          <List
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
            withPadding
          >
            <List.Item>Edit start time, end time, and intensity</List.Item>
            <List.Item>Delete the contraction if needed</List.Item>
          </List>
        </Stack>
        <Title order={3} mt="xl" visibleFrom="md">
          When to go to the hospital
        </Title>
        <Title order={4} mt="xl" hiddenFrom="md">
          When to go to the hospital
        </Title>
        <Stack gap="xs" mt={10}>
          <Text
            fw={500}
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
          >
            The app monitors your contractions and alerts you when:
          </Text>
          <List
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
            withPadding
          >
            <List.Item>
              It’s time to start preparing to go to the hospital
              <div style={{ marginTop: 6 }}>
                <PrepareForHospitalAlert />
              </div>
            </List.Item>
            <List.Item>
              It’s time to go to the hospital
              <div style={{ marginTop: 6 }}>
                <GoToHospitalAlert />
              </div>
            </List.Item>
          </List>

          <Text
            fw={500}
            size="sm"
            mt="xs"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
          >
            First-time mothers
          </Text>
          <List
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
            withPadding
          >
            <List.Item>
              First alert: last 4 contractions are 3 minutes apart and last 1 minute each
            </List.Item>
            <List.Item>Second alert: pattern holds for 1 hour (3‑1‑1)</List.Item>
          </List>

          <Text
            fw={500}
            size="sm"
            mt="xs"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
          >
            Have given birth before
          </Text>
          <List
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
            withPadding
          >
            <List.Item>
              First alert: last 4 contractions are 5 minutes apart and last 1 minute each
            </List.Item>
            <List.Item>Second alert: pattern holds for 1 hour (5‑1‑1)</List.Item>
          </List>

          <Text
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
            mt="xs"
          >
            You may not want to track continuously for an hour — consider going to hospital after
            the first alert if advised.
          </Text>

          <Text
            fw={500}
            size="sm"
            mt="xs"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
          >
            Please always follow your healthcare provider’s specific guidance.
          </Text>
        </Stack>
        <Title order={3} mt="xl" visibleFrom="md">
          When to contact a midwife
        </Title>
        <Title order={4} mt="xl" hiddenFrom="md">
          When to contact a midwife
        </Title>
        <Stack gap="xs" mt={10}>
          <Text
            fw={500}
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
          >
            Call your midwife or maternity unit for guidance if:
          </Text>
          <List
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
            withPadding
          >
            <List.Item>You think you’re in labour</List.Item>
            <List.Item>You’re having regular contractions every 5 minutes or more often</List.Item>
            <List.Item>You're worried about anything</List.Item>
          </List>

          <Text
            fw={500}
            size="sm"
            mt="xs"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
          >
            Call urgently if:
          </Text>
          <List
            size="sm"
            c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))"
            withPadding
          >
            <List.Item>Your waters break</List.Item>
            <List.Item>You have vaginal bleeding</List.Item>
            <List.Item>Your baby is moving less than usual</List.Item>
            <List.Item>You're under 37 weeks and think you might be in labour</List.Item>
            <List.Item>Any contraction lasts longer than 2 minutes</List.Item>
            <List.Item>You're having 6 or more contractions every 10 minutes</List.Item>
          </List>
          <Text size="sm" c="light-dark(var(--mantine-color-gray-8), var(--mantine-color-gray-0))">
            The app will alert you if you should call based on the final two points above.
          </Text>
          <CallMidwifeAlert />
          <Anchor
            href="https://www.nhs.uk/pregnancy/labour-and-birth/what-happens/the-stages-of-labour-and-birth/"
            target="_blank"
          >
            For additional information see this NHS page.
          </Anchor>
        </Stack>
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
