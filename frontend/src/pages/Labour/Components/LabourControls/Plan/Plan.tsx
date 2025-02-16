import { IconArrowRight, IconCalendar, IconPencil } from '@tabler/icons-react';
import { Button, Group, Image, Radio, Text, TextInput, Title } from '@mantine/core';
import { DatePickerInput } from '@mantine/dates';
import { useForm } from '@mantine/form';
import { ContainerHeader } from '../../../../../shared-components/ContainerHeader/ContainerHeader';
import image from './image.svg';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
import classes from './Plan.module.css';

export default function Plan({ setActiveTab }: { setActiveTab: Function }) {
  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      dueDate: undefined,
      firstLabour: 'true',
      labourName: '',
    },
  });
  return (
    <div className={baseClasses.root}>
      <ContainerHeader title="Plan" />
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title className={classes.title}>Plan your upcoming labour</Title>
            <Text c="var(--mantine-color-gray-7)" mt="md">
              Add some basic details about your upcoming labour to help us provide you with the best
              service.
            </Text>
            <Group mt={30}>
              <form
                onSubmit={form.onSubmit((values) => {
                  console.log(values);
                })}
              >
                <div className={classes.controls}>
                  <div className={classes.flexRow}>
                    <DatePickerInput
                      placeholder="Due date"
                      rightSection={<IconCalendar size={18} stroke={1.5} />}
                      label="Estimated due date"
                      description="Remember, your due date is only an estimate (only 4% of women give birth on theirs)"
                      radius="lg"
                      size="md"
                      required
                      key={form.key('dueDate')}
                      {...form.getInputProps('dueDate')}
                    />
                    <Radio.Group
                      name="firstLabour"
                      key={form.key('firstLabour')}
                      label="Is this your first labour?"
                      description="We use this information to make sure you get to hospital on time"
                      size="md"
                      withAsterisk
                      mt="20px"
                    >
                      <Group mt="xs">
                        <Radio value="true" label="Yes" />
                        <Radio value="false" label="No" />
                      </Group>
                    </Radio.Group>
                    <TextInput
                      rightSection={<IconPencil size={18} stroke={1.5} />}
                      label="Would you like to give your labour a name?"
                      description="You don't need to, but if you do we will use it when we send notifications to your subscribers"
                      placeholder="Baby Fern's birth"
                      size="md"
                      radius="lg"
                      mt="20px"
                    />
                  </div>
                </div>
              </form>
            </Group>
          </div>
          <Image src={image} className={classes.image} />
        </div>
        <div className={classes.submitRow}>
          <Button
            color="var(--mantine-color-pink-4)"
            rightSection={<IconArrowRight size={18} stroke={1.5} />}
            variant="filled"
            radius="xl"
            size="md"
            h={48}
            className={classes.submitButton}
            onClick={() => setActiveTab('details')}
            styles={{ section: { marginLeft: 22 } }}
            type="submit"
          >
            Finish Planning Labour
          </Button>
        </div>
      </div>
    </div>
  );
}
