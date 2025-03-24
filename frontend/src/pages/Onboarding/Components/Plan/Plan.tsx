import { useState } from 'react';
import { IconArrowRight, IconCalendar, IconPencil, IconUpload } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { Button, Group, Image, Radio, Text, TextInput, Title } from '@mantine/core';
import { DatePickerInput } from '@mantine/dates';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import { LabourDTO, LabourService, OpenAPI, PlanLabourRequest } from '../../../../client';
import image from './plan.svg';
import classes from './Plan.module.css';

export default function Plan({
  labour,
  gotoNextStep,
}: {
  labour: LabourDTO | undefined;
  gotoNextStep: Function;
}) {
  const auth = useAuth();
  const [mutationInProgress, setMutationInProgress] = useState<boolean>(false);

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const icon =
    labour === undefined ? (
      <IconArrowRight size={18} stroke={1.5} />
    ) : (
      <IconUpload size={18} stroke={1.5} />
    );

  const queryClient = useQueryClient();

  const boolToString = (val: boolean) => {
    return val ? 'true' : 'false';
  };

  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      dueDate: labour ? new Date(labour.due_date) : new Date(),
      firstLabour: labour ? boolToString(labour.first_labour) : 'true',
      labourName: labour ? labour.labour_name : '',
    },
  });

  const mutation = useMutation({
    mutationFn: async ({ values, existing }: { values: typeof form.values; existing: boolean }) => {
      setMutationInProgress(true);
      const requestBody: PlanLabourRequest = {
        due_date: values.dueDate.toISOString(),
        first_labour: values.firstLabour === 'true',
        labour_name: values.labourName,
      };
      let response;
      if (existing) {
        response = await LabourService.updateLabourPlanApiV1LabourPlanPut({ requestBody });
      } else {
        response = await LabourService.planLabourApiV1LabourPlanPost({ requestBody });
      }
      return response.labour;
    },
    onSuccess: async (labour) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
      gotoNextStep();
    },
    onError: async (error) => {
      notifications.show({
        title: 'Error Planning Labour',
        message: 'Something went wrong. Please try again.',
        radius: 'lg',
        color: 'var(--mantine-color-pink-7)',
      });
      console.error('Error planning labour', error);
      await new Promise((r) => setTimeout(r, 1000));
    },
    onSettled: () => {
      setMutationInProgress(false);
    },
  });

  return (
    <form
      onSubmit={form.onSubmit((values) =>
        mutation.mutate({ values, existing: labour !== undefined })
      )}
    >
      <div className={classes.inner} style={{ padding: 0, marginBottom: '25px' }}>
        <div className={classes.content}>
          <Title order={2}>Plan your upcoming labour</Title>
          <Text c="var(--mantine-color-gray-7)" mt="md">
            Add some basic details about your upcoming labour to help us provide you with the best
            service.
          </Text>
          <div className={classes.imageFlexRow}>
            <Image className={classes.smallImage} src={image} />
          </div>
          <Group mt={30}>
            <div className={classes.controls}>
              <div className={classes.flexRow}>
                <DatePickerInput
                  placeholder="Due date"
                  rightSection={<IconCalendar size={18} stroke={1.5} />}
                  valueFormat="DD/MM/YYYY"
                  label="Estimated due date"
                  description="Remember, your due date is only an estimate (only 4% of women give birth on theirs)"
                  radius="lg"
                  size="md"
                  required
                  key={form.key('dueDate')}
                  {...form.getInputProps('dueDate')}
                  withAsterisk
                />
                <Radio.Group
                  name="firstLabour"
                  key={form.key('firstLabour')}
                  label="Is this your first labour?"
                  description="We use this information to make sure you get to hospital on time"
                  size="md"
                  withAsterisk
                  {...form.getInputProps('firstLabour')}
                  mt="20px"
                >
                  <Group mt="xs">
                    <Radio value="true" label="Yes" />
                    <Radio value="false" label="No" />
                  </Group>
                </Radio.Group>
                <TextInput
                  rightSection={<IconPencil size={18} stroke={1.5} />}
                  key={form.key('labourName')}
                  label="Would you like to give your labour a name?"
                  description="You don't need to, but if you do we will use it when we send notifications to your subscribers"
                  placeholder="Baby Fern's birth"
                  size="md"
                  radius="lg"
                  {...form.getInputProps('labourName')}
                  mt="20px"
                />
              </div>
            </div>
          </Group>
        </div>
        <Image src={image} className={classes.image} />
      </div>
      {(labour === undefined && (
        <div
          className={classes.submitRow}
          style={{ justifyContent: 'flex-end', marginTop: '15px' }}
        >
          <Button
            color="var(--mantine-color-pink-4)"
            rightSection={icon}
            variant="filled"
            radius="xl"
            size="md"
            h={48}
            className={classes.submitButton}
            styles={{ section: { marginLeft: 22 } }}
            type="submit"
            loading={mutationInProgress}
          >
            Finish Planning Labour
          </Button>
        </div>
      )) || (
        <div className={classes.submitRow} style={{ justifyContent: 'space-between' }}>
          <Button
            color="var(--mantine-color-pink-4)"
            leftSection={icon}
            variant="light"
            radius="xl"
            size="md"
            h={48}
            className={classes.submitButton}
            styles={{ section: { marginRight: 22 } }}
            type="submit"
            loading={mutationInProgress}
          >
            Update labour plan
          </Button>
          <Button
            color="var(--mantine-color-pink-4)"
            rightSection={<IconArrowRight size={18} stroke={1.5} />}
            variant="filled"
            radius="xl"
            size="md"
            h={48}
            className={classes.backButton}
            styles={{ section: { marginLeft: 22 } }}
            onClick={() => gotoNextStep()}
          >
            Next step
          </Button>
        </div>
      )}
    </form>
  );
}
