import { Title, Space, Text } from '@mantine/core'
import { formatTimeSeconds } from '../utils'
import { LabourDTO } from '../../client'
import baseClasses from '../shared-styles.module.css'
import classes from './LabourStatistics.module.css'
import { LabourStatisticsTabs } from './LabourStatisticsTabs'

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
            {!completed && !labour.statistics.total && 
                <Text className={classes.labourStatsText}>Not enough data yet, keep tracking.</Text>
            }
            {labour.statistics.total &&
                <LabourStatisticsTabs statistics={labour.statistics} />
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
