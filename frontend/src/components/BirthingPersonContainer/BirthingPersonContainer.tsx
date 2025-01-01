import { Space, Stack, Text, Title } from '@mantine/core';
import classes from './BirthingPersonContainer.module.css';
import { BirthingPersonDTO } from '../../client';


export default function BirthingPersonContainer({ birthingPerson }: { birthingPerson: BirthingPersonDTO }) {
  return (
    <div className={classes.wrapper}>
      <div className={classes.body} >
        <Stack align='flex-start' justify='center' gap='md'>
          <Title fz="xl" className={classes.title}>{birthingPerson.first_name} {birthingPerson.last_name}</Title>
          <Text fz="md">Labour Summary Here</Text>
          <Space h="lg" />
        </Stack>
      </div>
    </div>
  )
}
