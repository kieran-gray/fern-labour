import { useEffect, useRef, useState } from 'react';
import { IconClock, IconUpload } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button, Modal, ScrollArea, Slider, Space, Text, Timeline } from '@mantine/core';
import { TimeInput } from '@mantine/dates';
import { useForm } from '@mantine/form';
import { useDisclosure } from '@mantine/hooks';
import { notifications } from '@mantine/notifications';
import {
  ContractionDTO,
  LabourService,
  OpenAPI,
  UpdateContractionRequest,
} from '../../../../client';
import {
  formatTimeMilliseconds,
  formatTimeSeconds,
  getTimeSinceLastStarted,
} from '../../../../shared-components/utils';
import modalClasses from '../../../../shared-components/Modal.module.css';
import classes from './Contractions.module.css';

const DOTTED_LINE_FREQUENCY_GAP = 1800000;

export interface ContractionData {
  contractionId: string;
  startTime: string;
  endTime: string;
  intensity: number | null;
}

export default function ContractionTimeline({ contractions }: { contractions: ContractionDTO[] }) {
  const auth = useAuth();

  const [opened, { open, close }] = useDisclosure(false);
  const [contractionData, setContractionData] = useState<ContractionData | null>(null);
  const [mutationInProgress, setMutationInProgress] = useState<boolean>(false);

  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      startTime: '',
      endTime: '',
      intensity: 5,
    },
  });

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const queryClient = useQueryClient();

  const viewport = useRef<HTMLDivElement>(null);
  const formatIntensity = (intensity: number | null): string => {
    return intensity ? intensity.toString() : '0';
  };
  const contractionFrequencyGaps = getTimeSinceLastStarted(contractions);

  const setClickedContractionData = (contraction: ContractionDTO) => {
    const contractionData: ContractionData = {
      contractionId: contraction.id,
      startTime: contraction.start_time,
      endTime: contraction.end_time,
      intensity: contraction.intensity,
    };
    setContractionData(contractionData);
  };

  const updateTime = (dateTime: string, time: string) => {
    const split = dateTime.split("T")
    split[1] = `${time}Z`
    return split.join("T")
  }

  const mutation = useMutation({
    mutationFn: async ({
      values,
      contractionId,
    }: {
      values: typeof form.values;
      contractionId: string;
    }) => {
      setMutationInProgress(true);
      const startTime = values.startTime !== '' ? updateTime(contractionData!.startTime, values.startTime) : contractionData!.startTime;
      const endTime = values.endTime !== '' ? updateTime(contractionData!.endTime, values.endTime) : contractionData!.endTime;

      const requestBody: UpdateContractionRequest = {
        start_time: startTime,
        end_time: endTime,
        intensity: values.intensity,
        contraction_id: contractionId,
      };
      const response = await LabourService.updateContractionApiV1LabourContractionUpdatePut({
        requestBody,
      });
      return response.labour;
    },
    onSuccess: async (labour) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
      setMutationInProgress(false);
      notifications.show({
        title: 'Success',
        message: `Contraction Updated`,
        radius: 'lg',
        color: 'var(--mantine-color-green-3)',
      });
      close()
    },
    onError: async (_) => {
      setMutationInProgress(false);
      notifications.show({
        title: 'Error Updating Contraction',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
    },
    onSettled: () => {
      form.reset();
    }
  });

  const timelineContractions = contractions.map((contraction) => (
    <Timeline.Item
      fs="xl"
      fw={1000}
      bullet={
        <Text className={classes.bulletText}>
          {contraction.start_time !== contraction.end_time &&
            formatIntensity(contraction.intensity)}
        </Text>
      }
      onClick={() => {
        setClickedContractionData(contraction);
        if (contraction.start_time !== contraction.end_time) {
          open();
        }
      }}
      key={contraction.id}
      style={{ cursor: contraction.start_time !== contraction.end_time ? 'pointer' : 'default' }}
      title=""
      lineVariant={
        contractionFrequencyGaps[contraction.id].next > DOTTED_LINE_FREQUENCY_GAP
          ? 'dotted'
          : 'solid'
      }
    >
      <Text className={classes.timelineLabel}>
        Start Time:{' '}
        <strong>
          {new Date(contraction.start_time).toLocaleTimeString(navigator.language, {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </strong>
      </Text>
      {contractionFrequencyGaps[contraction.id].previous !== 0 && (
        <Text className={classes.timelineLabel}>
          Frequency:{' '}
          <strong>
            {formatTimeMilliseconds(contractionFrequencyGaps[contraction.id].previous)}
          </strong>
        </Text>
      )}
      {contraction.start_time !== contraction.end_time && (
        <Text className={classes.timelineLabel}>
          Duration: <strong>{formatTimeSeconds(contraction.duration)}</strong>
        </Text>
      )}
      {contractionFrequencyGaps[contraction.id].previous === 0 && <br />}
      {contraction.notes && <Text className={classes.timelineLabel}>{contraction.notes}</Text>}
      <Space h="md" />
    </Timeline.Item>
  ));

  useEffect(() => {
    if (viewport.current) {
      viewport.current.scrollTo({ top: viewport.current.scrollHeight, behavior: 'auto' });
    }
  }, [timelineContractions]);

  return (
    <>
      <Modal
        opened={opened}
        onClose={close}
        title="Update Contraction"
        centered
        overlayProps={{ backgroundOpacity: 0.55, blur: 3 }}
        classNames={{
          content: modalClasses.modalRoot,
          header: modalClasses.modalHeader,
          title: modalClasses.modalTitle,
          body: modalClasses.modalBody,
          close: modalClasses.closeButton,
        }}
      >
        <form
          onSubmit={form.onSubmit((values) =>
            mutation.mutate({ values, contractionId: contractionData!.contractionId })
          )}
        >
          <Space h="lg" />
          <TimeInput
            rightSection={<IconClock />}
            withSeconds
            key={form.key('startTime')}
            radius="lg"
            label="Start Time"
            {...form.getInputProps('startTime')}
            defaultValue={contractionData?.startTime.split('T')[1].slice(0, 8) || undefined}
          />
          <Space h="lg" />
          <TimeInput
            rightSection={<IconClock />}
            withSeconds
            key={form.key('endTime')}
            radius="lg"
            label="End Time"
            {...form.getInputProps('endTime')}
            defaultValue={contractionData?.endTime.split('T')[1].slice(0, 8) || undefined}
          />
          <Space h="lg" />
          <Slider
            classNames={{
              root: classes.slider,
              markLabel: classes.markLabel,
              track: classes.track,
            }}
            
            color="var(--mantine-color-pink-4)"
            key={form.key('intensity')}
            size="xl"
            radius="lg"
            min={0}
            max={10}
            step={1}
            {...form.getInputProps('intensity')}
            defaultValue={contractionData?.intensity || 5}
            marks={[
              { value: 0, label: '0' },
              { value: 5, label: 5 },
              { value: 10, label: 10 },
            ]}
          />
          <Space h="xl" />
          <Button
            color="var(--mantine-color-pink-4)"
            leftSection={<IconUpload />}
            variant="outline"
            radius="xl"
            size="md"
            h={48}
            className={classes.submitButton}
            styles={{ section: { marginRight: 22 } }}
            style={{width: '100%'}}
            type="submit"
            loading={mutationInProgress}
          >
            Update Contraction
          </Button>
        </form>
      </Modal>
      <ScrollArea.Autosize mah={500} viewportRef={viewport}>
        <Timeline
          ml={30}
          active={timelineContractions.length}
          lineWidth={6}
          bulletSize={60}
          color="var(--mantine-color-pink-4)"
        >
          {timelineContractions}
        </Timeline>
      </ScrollArea.Autosize>
    </>
  );
}
