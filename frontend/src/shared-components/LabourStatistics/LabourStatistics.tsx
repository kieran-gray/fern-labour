import { Title, Space, Text } from '@mantine/core'
import { formatTimeSeconds } from '../utils'
import { LabourDTO } from '../../client'
import baseClasses from '../shared-styles.module.css'
import classes from './LabourStatistics.module.css'

export const LabourStatistics = ({labour, completed, inContainer = true}: {labour: LabourDTO, completed: boolean, inContainer?: boolean}) => {
    const statistics = (
            <>
            <Text className={classes.labourStatsText}>Start Time: <strong>{new Date(labour.start_time).toString().slice(0, 21)}</strong></Text>
            {labour.end_time &&
            <>
                <Text className={classes.labourStatsText}>
                    End Time: <strong>{new Date(labour.end_time).toString().slice(0, 21)}</strong>
                </Text>
                <Text className={classes.labourStatsText}>
                    Duration: <strong>{formatTimeSeconds((new Date(labour.end_time).getTime() - new Date(labour.start_time).getTime())/1000, true)}</strong>
                </Text>
            </> ||
                <Text className={classes.labourStatsText}>
                    Elapsed Time: <strong>{formatTimeSeconds((new Date().getTime() - new Date(labour.start_time).getTime())/1000, true)}</strong>
                </Text>
            }
            <Space h="sm" />

            <Text className={classes.labourStatsText}>Number of contractions: <strong>{labour.contractions.length}</strong></Text>
            { (labour.pattern && !labour.end_time)&& 
            <>
                <Space h="sm" />
                {!completed &&
                    <Text className={classes.labourStatsText}>
                        Contractions in last hour: <strong>{labour.pattern.contractions_in_last_hour}</strong>
                    </Text>
                }

                <Space h="sm" />
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
                <Text className={classes.labourStatsText}>(Averaged over your last {labour.contractions.length < 10 ? labour.contractions.length : 10} contractions)</Text>
            </> || !completed && 
            <Text className={classes.labourStatsText}>Not enough data yet, keep tracking.</Text>
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
