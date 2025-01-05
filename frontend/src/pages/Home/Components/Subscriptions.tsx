import { Badge, Text } from '@mantine/core';
import baseClasses from '../../../shared-components/shared-styles.module.css';
import { BirthingPersonSummaryDTO } from '../../../client';


export default function Subscriptions({ subscriptions }: { subscriptions: BirthingPersonSummaryDTO[] }) {
  const formatLabourDurationHours = (hours: number): string => {
    const wholeHours = Math.round(hours);
    if (wholeHours < 1) {
      return "Less than 1 hour"
    } else if (wholeHours == 1) {
      return `${wholeHours} hour`
    } else {
      return `${wholeHours} hours`
    }
  }


  const subscriptionsElements = subscriptions.map((subscription) => (
    <div key={subscription.id} className={baseClasses.body}>
      <div className={baseClasses.flexRowNoBP}>
        <Text className={baseClasses.text}>{subscription.first_name} {subscription.last_name}</Text>
        <Badge size='lg' mb={20} pl={40} pr={40} variant="light">{subscription.active_labour ? 'In Labour' : 'Not In Labour'}</Badge>
      </div>
      {subscription.active_labour && 
        <>
          <Text className={baseClasses.text}>Number of contractions: {subscription.active_labour.contraction_count}</Text>
          <Text className={baseClasses.text}></Text>
          <Text className={baseClasses.text}>Labour duration: {formatLabourDurationHours(subscription.active_labour.duration)}</Text>
          <Text className={baseClasses.text}>Current phase: {subscription.active_labour.current_phase}</Text>
          <Text className={baseClasses.text}>Hospital recommended: {String(subscription.active_labour.hospital_recommended)}</Text>
        </>
      }
    </div>
  ));
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.header}>
        <div className={baseClasses.title}>Your subscriptions</div>
      </div>
      {subscriptionsElements}
      {subscriptions.length == 0 && 
        <div className={baseClasses.body}>
          <div className={baseClasses.text}>Subscribe to someone to see their labour details here</div>
        </div>
      }
      
  </div>
  )
}
