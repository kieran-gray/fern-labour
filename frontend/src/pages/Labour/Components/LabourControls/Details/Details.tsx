import { IconArrowLeft, IconArrowRight } from '@tabler/icons-react';
import { Badge, Button, Text, Title } from '@mantine/core';
import { ContainerHeader } from '../../../../../shared-components/ContainerHeader/ContainerHeader';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
import classes from './Details.module.css';

const data = {
  dueDate: 'February 1, 2025',
  firstLabour: true,
  labourName: "Baby Fern's Birth",
};

export default function Details({ setActiveTab }: { setActiveTab: Function }) {
  return (
    <div className={baseClasses.root}>
      <ContainerHeader title="Details" />
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title className={classes.title}>
              {data.labourName ? data.labourName : 'Your Labour'}
            </Title>
            <Text c="var(--mantine-color-gray-7)" mt="md" mb="md">
              Take a deep breath—you’ve got this! Here, you can check your labour details and start
              tracking contractions when they kick in.
            </Text>
            <div className={classes.infoRow}>
              <Badge variant="filled" className={classes.labourBadge} size="lg">
                Not in labour
              </Badge>
              <Badge variant="filled" className={classes.labourBadge} size="lg">
                Due: {data.dueDate}
              </Badge>
              <Badge variant="filled" className={classes.labourBadge} size="lg">
                Gestational age: 42 weeks + 1 day
              </Badge>
              <Badge variant="filled" className={classes.labourBadge} size="lg">
                {!data.firstLabour ? 'Not ' : ''}first time mother
              </Badge>
            </div>
            <div className={baseClasses.flexRow} style={{ marginTop: '20px' }}>
              <Button
                color="var(--mantine-color-pink-4)"
                leftSection={<IconArrowLeft size={18} stroke={1.5} />}
                variant="outline"
                radius="xl"
                size="md"
                h={48}
                className={classes.backButton}
                onClick={() => setActiveTab('plan')}
                type="submit"
              >
                Go back to planning
              </Button>
              <Button
                color="var(--mantine-color-pink-4)"
                rightSection={<IconArrowRight size={18} stroke={1.5} />}
                variant="filled"
                radius="xl"
                size="md"
                h={48}
                onClick={() => setActiveTab('complete')}
                type="submit"
              >
                Complete your labour
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
