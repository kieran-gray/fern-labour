import { Grid, Space, Stack, Text, Title } from '@mantine/core';
import classes from './LabourContainer.module.css';
import { LabourDTO } from '../../client';
import ContractionList from '../ContractionList/ContractionList';
import StartContractionButton from '../Buttons/StartContractionButton/StartContractionButton';
import EndContractionButton from '../Buttons/EndContractionButton/EndContractionButton';
import CompleteLabourButton from '../Buttons/CompleteLabourButton/CompleteLabourButton';
import BeginLabourButton from '../Buttons/BeginLabourButton/BeginLabourButton';


export default function LabourContainer({labour, hasActiveLabour, setLabour}: { labour: LabourDTO | null, hasActiveLabour: boolean | null, setLabour: Function }) {
  if (hasActiveLabour && labour) {
    const hasActiveContraction = labour.contractions.some(contraction => contraction.is_active)
    return (
      <div className={classes.wrapper}>
        <div className={classes.body} >
          <Grid grow gutter='xl' w="100%" h="100%">
            <Grid.Col span="auto" w="100%">
              <Stack align='flex-start' justify='center' gap='md'>
                <Title fz="xl" className={classes.title}>Your Labour</Title>
                <Text fz="sm">Start Time: {labour.start_time}</Text>
                <Text fz="sm">Current Phase: {labour.current_phase}</Text>
                <Space h="lg" />
                
              </Stack>
            </Grid.Col>
            <Grid.Col span="auto" w="100%">
              <Stack align='stretch' justify='center' gap='md'>
              <Space h="xl" />
                <CompleteLabourButton setLabour={setLabour}/>
              </Stack>
            </Grid.Col>
          </Grid>
          <Space h="md" />
          <Grid grow gutter='xl' w="100%" h="100%">
            <Grid.Col span="auto" w="100%">
              <Stack align='stretch' justify='flex-end' h="100%">
              <Text fw={500} fz="md" mb={5}>Your contractions will appear below</Text>
                <ContractionList contractions={labour.contractions} />
              </Stack>
            </Grid.Col>
            <Grid.Col span="auto" w="100%">
              <Stack align='stretch' justify='flex-end' h="100%">
                  {hasActiveContraction && <EndContractionButton setLabour={setLabour} />}
                  {!hasActiveContraction && <StartContractionButton setLabour={setLabour}/>}
                </Stack>
            </Grid.Col>
          </Grid>
        </div>
      </div>
    )
  } else {
    return (
      <div className={classes.wrapper}>
        <div className={classes.body}>
          <Title fz="xl" className={classes.title}>Begin Labour</Title>
          <Text fw={500} fz="md" mb={5}>You're not currently in active labour.</Text>
          <Text fw={500} fz="md" mb={5}>Click the button below to begin</Text>
          <Space h="xl"></Space>
          <BeginLabourButton setLabour={setLabour}/>
        </div>
      </div>
    )
  }
}
