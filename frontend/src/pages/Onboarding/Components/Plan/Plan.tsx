import { validateLabourName } from '@base/shared-components/utils';
import { LabourDTO, PlanLabourRequest } from '@clients/labour_service';
import { usePlanLabour } from '@shared/hooks';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { IconArrowRight, IconCalendar, IconPencil, IconUpload } from '@tabler/icons-react';
import { useNavigate } from 'react-router-dom';
import { Button, Group, Image, Radio, TextInput } from '@mantine/core';
import { DatePickerInput } from '@mantine/dates';
import { useForm } from '@mantine/form';
import image from './plan.svg';
import classes from './Plan.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export default function Plan({ labour }: { labour: LabourDTO | undefined }) {
  const navigate = useNavigate();
  const planLabourMutation = usePlanLabour();

  const icon =
    labour === undefined ? (
      <IconArrowRight size={18} stroke={1.5} />
    ) : (
      <IconUpload size={18} stroke={1.5} />
    );

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
    validate: { labourName: (value) => validateLabourName(value) },
  });

  const handlePlanLabour = (values: typeof form.values) => {
    const requestBody: PlanLabourRequest = {
      due_date: values.dueDate.toISOString(),
      first_labour: values.firstLabour === 'true',
      labour_name: values.labourName,
    };
    const existing = labour !== undefined;
    planLabourMutation.mutate({ requestBody, existing });
    if (!existing) {
      setTimeout(() => navigate('/'), 100);
    }
  };

  const title = 'Plan your upcoming labour';
  const description =
    'Add some basic details about your upcoming labour to help us provide you with the best service.';

  return (
    <form onSubmit={form.onSubmit((values) => handlePlanLabour(values))}>
      <div className={classes.inner} style={{ padding: 0, marginBottom: '25px' }}>
        <div className={classes.content}>
          <ResponsiveTitle title={title} />
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
            loading={planLabourMutation.isPending}
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
            loading={planLabourMutation.isPending}
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
