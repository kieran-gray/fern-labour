import { Title, Space, Text } from '@mantine/core'
import { formatTimeSeconds } from '../utils'
import { LabourSummaryDTO } from '../../client'
import baseClasses from '../shared-styles.module.css'
import classes from './LabourStatistics.module.css'

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

export const LabourSummaryStatistics = ({labour, inContainer = true}: {labour: LabourSummaryDTO, inContainer?: boolean}) => {
    const statistics = (
        <>
          <Text className={classes.labourStatsText}>
            Labour duration: <strong>{formatLabourDurationHours(labour.duration)}</strong>
          </Text>
          <Text className={classes.labourStatsText}>
            Current phase: <strong>{labour.current_phase}</strong>
            </Text>
          <Text className={classes.labourStatsText}>
            Hospital recommended: <strong>{String(labour.hospital_recommended)}</strong>
            </Text>


            <Text className={classes.labourStatsText}>Total number of contractions: <strong>{labour.contraction_count}</strong></Text>
            { labour.pattern && 
            <>
                <Space h="sm" />
                <Text className={classes.labourStatsText}>
                    Contractions in last hour: <strong>{labour.pattern.contractions_in_last_hour}</strong>
                </Text>
                <Text className={classes.labourStatsText}>
                Average contraction duration: <strong>{formatTimeSeconds(labour.pattern.average_duration)}</strong>
                </Text>
                <Text className={classes.labourStatsText}>
                Average contraction interval: <strong>{formatTimeSeconds(labour.pattern.average_interval)}</strong>
                </Text>
                <Text className={classes.labourStatsText}>
                Average contraction intensity: <strong>{labour.pattern.average_intensity} out of 10</strong>
                </Text>
                <Space h="sm" />
                <Text className={classes.labourStatsText}>
                    (Averaged over the last {labour.contraction_count < 10 ? labour.contraction_count : 10} contractions)
                </Text>
            </>
            }
        </>
    )
    if (inContainer) {
        return (
            <div className={baseClasses.root}>
                <div className={baseClasses.header}>
                    <Title fz="xl" className={baseClasses.title}>Your Labour Statistics</Title>
                </div>
                <div className={baseClasses.body}>
                    {statistics}
                </div>
            </div>
        )
    } else {
        return (
            statistics
        )
    }
}
