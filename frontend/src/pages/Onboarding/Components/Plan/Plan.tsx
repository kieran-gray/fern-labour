import { useState } from 'react';
import { LabourDTO, LabourService, OpenAPI, PlanLabourRequest } from '@clients/labour_service';
import { Error, Success } from '@shared/Notifications';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { IconArrowRight, IconCalendar, IconPencil, IconUpload } from '@tabler/icons-react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Button, Group, Image, Radio, TextInput, Title } from '@mantine/core';
import { DatePickerInput } from '@mantine/dates';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';
import image from './plan.svg';
import classes from './Plan.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export default function Plan({ labour }: { labour: LabourDTO | undefined }) {
  const navigate = useNavigate();
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
        response = await LabourService.updateLabourPlan({ requestBody });
      } else {
        response = await LabourService.planLabour({ requestBody });
      }
      return response.labour;
    },
    onSuccess: async (labour, variables) => {
      queryClient.setQueryData(['labour', auth.user?.profile.sub], labour);
      const message = variables.existing ? 'Labour Plan Updated' : 'Labour Planned';
      notifications.show({
        ...Success,
        title: 'Success',
        message,
      });
    },
    onError: async (error) => {
      notifications.show({
        ...Error,
        title: 'Error Planning Labour',
        message: 'Something went wrong. Please try again.',
      });
      console.error('Error planning labour', error);
    },
    onSettled: () => {
      setMutationInProgress(false);
    },
  });

  const title = 'Plan your upcoming labour';
  const description =
    'Add some basic details about your upcoming labour to help us provide you with the best service.';

  return (
    <form
      onSubmit={form.onSubmit((values) =>
        mutation.mutate({ values, existing: labour !== undefined })
      )}
    >
      <div className={classes.inner} style={{ padding: 0, marginBottom: '25px' }}>
        <div className={classes.content}>
          <Title order={3} hiddenFrom="sm">
            {title}
          </Title>
          <Title order={2} visibleFrom="sm">
            {title}
          </Title>
          <ResponsiveDescription description={description} marginTop={10} />
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
                  styles={{
                    weekday: {
                      color: 'light-dark(var(--mantine-color-gray-6), var(--mantine-color-gray-4))',
                    },
                  }}
                  classNames={{
                    description: baseClasses.description,
                    input: baseClasses.input,
                    section: baseClasses.section,
                    levelsGroup: baseClasses.selectDropdown,
                  }}
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
                  classNames={{ description: baseClasses.description }}
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
                  classNames={{
                    description: baseClasses.description,
                    input: baseClasses.input,
                    section: baseClasses.section,
                  }}
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
            color="var(--mantine-primary-color-4)"
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
            color="var(--mantine-primary-color-4)"
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
            color="var(--mantine-primary-color-4)"
            rightSection={<IconArrowRight size={18} stroke={1.5} />}
            variant="filled"
            radius="xl"
            size="md"
            h={48}
            className={classes.backButton}
            styles={{ section: { marginLeft: 22 } }}
            onClick={() => navigate('/')}
          >
            Go to app
          </Button>
        </div>
      )}
    </form>
  );
}
