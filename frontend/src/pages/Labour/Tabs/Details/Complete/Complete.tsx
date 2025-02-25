import { useState } from 'react';
import { IconArrowLeft, IconPencil } from '@tabler/icons-react';
import { Button, Image, Text, Textarea, Title } from '@mantine/core';
import { ContainerHeader } from '../../../../../shared-components/ContainerHeader/ContainerHeader';
import CompleteLabourButton from './CompleteLabourButton';
import image from './image.svg';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
import classes from './Complete.module.css';

export default function Complete({
  activeContraction,
  setActiveTab,
}: {
  activeContraction: boolean;
  setActiveTab: Function;
}) {
  const [labourNotes, setLabourNotes] = useState('');
  return (
    <div className={baseClasses.root}>
      <ContainerHeader title="Complete" />
      <div className={baseClasses.body}>
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title className={classes.title}>Complete your labour</Title>
            <div className={baseClasses.flexRow} style={{ flexWrap: 'nowrap' }}>
              <Text c="var(--mantine-color-gray-7)" mt="md" mb="md" size="md">
                You did it! Bringing new life into the world is an incredible journey, and we are so
                proud of you. Take a deep breath, soak in this beautiful moment, and know that you
                are amazing.
                <br />
                <br />
                If you want to, you can add a note below before completing your labour which will be
                shared with all of your subscribers.
                <br />
                <br />
                You could use it to introduce the new addition to your family, or just to let
                everyone know you are OK.
              </Text>
              <Image src={image} className={classes.image} style={{ flexGrow: 1 }} />
            </div>
            <div className={baseClasses.flexColumn}>
              <Textarea
                rightSection={<IconPencil size={18} stroke={1.5} />}
                radius="lg"
                size="md"
                placeholder="Your closing note"
                classNames={{
                  label: classes.labourNotesLabel,
                }}
                onChange={(event) => setLabourNotes(event.currentTarget.value)}
              />

              <div className={baseClasses.flexRow} style={{ marginTop: '20px' }}>
                <Button
                  color="var(--mantine-color-pink-4)"
                  leftSection={<IconArrowLeft size={18} stroke={1.5} />}
                  variant="outline"
                  radius="xl"
                  size="md"
                  h={48}
                  className={classes.backButton}
                  onClick={() => setActiveTab('details')}
                  type="submit"
                >
                  Go back to labour
                </Button>
                <CompleteLabourButton disabled={!!activeContraction} labourNotes={labourNotes} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
