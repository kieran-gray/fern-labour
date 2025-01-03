import { Grid, Slider, Space, Stack, Text, Textarea, Title } from '@mantine/core';
import classes from './LabourContainer.module.css';
import baseClasses from '../shared-styles.module.css';
import { LabourDTO } from '../../client';
import ContractionList from '../ContractionList/ContractionList';
import StartContractionButton from '../Buttons/StartContractionButton/StartContractionButton';
import EndContractionButton from '../Buttons/EndContractionButton/EndContractionButton';
import CompleteLabourButton from '../Buttons/CompleteLabourButton/CompleteLabourButton';
import BeginLabourButton from '../Buttons/BeginLabourButton/BeginLabourButton';
import { useState } from 'react';


export default function LabourContainer({ labour, hasActiveLabour, setLabour }: { labour: LabourDTO | null, hasActiveLabour: boolean | null, setLabour: Function }) {
  const [intensity, setIntensity] = useState(5);
  const [labourNotes, setLabourNotes] = useState("");

  const formatTimeGap = (milliseconds: number) => {
    if (milliseconds === 0) {
      return null
    }
    const seconds = Math.floor(milliseconds / 1000);
    if (seconds < 60) {
      return `${seconds} seconds`
    }
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60;
    return `${minutes} minute${minutes > 1 ? 's' : ''} ${remainingSeconds} seconds`;
  }
  window.scrollTo(0, document.body.scrollHeight);
  if (hasActiveLabour && labour) {

    const sortedContractions = labour?.contractions.sort(
      (a,b) => (a.start_time < b.start_time) ? -1 : ((a.start_time > b.start_time) ? 1 : 0)
    );
    const timeSinceLastEnded: Record<string, string | null> = {};
    let lastEndTime: string = "";
  
    sortedContractions.forEach(contraction => {
      const gap = lastEndTime ? 
        new Date(contraction.start_time).getTime() - new Date(lastEndTime).getTime() : 0;
      timeSinceLastEnded[contraction.id] = formatTimeGap(gap)
      lastEndTime = contraction.end_time;
    });
    const hasActiveContraction = labour.contractions.some(contraction => contraction.is_active)
    return (
      <div className={baseClasses.flexColumn}>
      <div className={baseClasses.root}>
        <div className={baseClasses.header}>
          <Title fz="xl" className={baseClasses.title}>Your Labour</Title>
        </div>
        <div className={baseClasses.body}>
          <div>
            <div className={baseClasses.flexColumn}>
            <Stack align='flex-start' justify='center' gap='md' miw={200}>
                <Text className={baseClasses.text}>Start Time: {new Date(labour.start_time).toString().slice(0, 24)}</Text>
                <Text className={baseClasses.text}>Current Phase: {labour.current_phase.toUpperCase()}</Text>
                <Space h="lg" />
            </Stack>
            <Stack align='stretch' justify='flex-end' h="100%">
                <Text className={baseClasses.text}>Your contractions{sortedContractions.length > 0 && ":" || " will appear below"}</Text>
                <ContractionList contractions={sortedContractions} contractionGaps={timeSinceLastEnded} />
              </Stack>
            </div>
            <div className={baseClasses.flexColumnEnd}>
              <Space h="xl" />
              <Stack align='stretch' justify='flex-end' h="100%">
                {hasActiveContraction &&
                  <>
                    <Text className={baseClasses.minorText}>Set your contraction intensity before completing the contraction</Text>
                    <Slider
                      classNames={{ root: classes.slider, markLabel: classes.markLabel, track: classes.track }}
                      color="var(--mantine-color-pink-4)"
                      size="xl"
                      radius="lg"
                      min={0}
                      max={10}
                      step={1}
                      defaultValue={5}
                      onChange={setIntensity}
                      marks={[
                        { value: 0, label: '0' },
                        { value: 5, label: 5 },
                        { value: 10, label: 10 }
                      ]}
                    />
                    <EndContractionButton intensity={intensity} setLabour={setLabour} />
                  </>
                }
                {!hasActiveContraction && <StartContractionButton setLabour={setLabour} />}
              </Stack>
            </div>
          </div>
        </div>
      </div>
      <Space h="xl" />
      <div className={baseClasses.root}>
        <div className={baseClasses.header}>
          <Title fz="xl" className={baseClasses.title}>Complete Your Labour</Title>
        </div>
        <div className={baseClasses.body}>
          <Stack align='stretch' justify='center' gap='md'>
            <Textarea radius="lg" label="Your labour notes" description="These notes will be shared with your subscribers when you complete your labour." classNames={{ label: classes.labourNotesLabel, description: classes.labourNotesDescription}} onChange={(event) => setLabourNotes(event.currentTarget.value)}/>
            <CompleteLabourButton setLabour={setLabour} disabled={hasActiveContraction} labourNotes={labourNotes}/>
          </Stack>
        </div>
        </div>
      </div>
    )
  } else {
    return (
      <div className={baseClasses.root}>
        <div className={baseClasses.header}>
          <Title fz="xl" className={baseClasses.title}>Begin Labour</Title>
        </div>
        <div className={baseClasses.body}>
            <Text className={baseClasses.text}>You're not currently in active labour.</Text>
            <Text className={baseClasses.text}>Click the button below to begin</Text>
            <Space h="xl"></Space>
            <BeginLabourButton setLabour={setLabour} />
        </div>
      </div>
    )
  }
}
