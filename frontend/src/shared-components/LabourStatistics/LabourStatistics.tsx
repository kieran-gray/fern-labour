import { Title, Space, Text } from '@mantine/core'
import { formatTimeSeconds } from '../utils'
import { LabourDTO } from '../../client'
import baseClasses from '../shared-styles.module.css'
import classes from './LabourStatistics.module.css'

export const LabourStatistics = ({labour, inContainer = false}: {labour: LabourDTO, inContainer?: boolean}) => {
    const statistics = (
            <>
            <Text className={classes.labourStatsText}>Start Time: <strong>{new Date(labour.start_time).toString().slice(0, 21)}</strong></Text>
            <Space h="sm" />
            <Text className={classes.labourStatsText}>Number of contractions: <strong>{labour.contractions.length}</strong></Text>
            { labour.pattern && 
            <>
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
                <Text className={classes.markLabel}>(Averaged over your last {labour.contractions.length < 10 ? labour.contractions.length : 10} contractions)</Text>
            </> ||
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
