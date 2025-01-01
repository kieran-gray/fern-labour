import { Space, Stack, Text, Title } from '@mantine/core';
import classes from './SubscriptionsContainer.module.css';
import { BirthingPersonSummaryDTO } from '../../client';
import { SubscriptionsTable } from '../SubscriptionsTable/SubscriptionsTable';


export default function SubscriptionsContainer({subscriptions}: {subscriptions: BirthingPersonSummaryDTO[]}) {
  console.log(subscriptions)
  const birthingPersonList = subscriptions.map((subscription) => (
    <Stack align='flex-start' justify='center' gap='md'>
      <Title fz="md" className={classes.title}>{subscription.first_name} {subscription.last_name}</Title>
      <Text fz="md">Labour Summary Here</Text>
      <Space h="lg" />
    </Stack>
    ));
  return (
    <div className={classes.wrapper}>
      <div className={classes.body} >
        <Title fz="xl" className={classes.title}>Subscriptions:</Title>
        { birthingPersonList.length > 0 && <SubscriptionsTable subscriptions={subscriptions} />}
        { birthingPersonList.length == 0 && <Text fz="md">Anyone that you subscribe to will show up below.</Text>}
      </div>
    </div>
  )
}
