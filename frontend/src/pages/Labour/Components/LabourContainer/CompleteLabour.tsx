import { Stack, Textarea, Title } from '@mantine/core'
import classes from './LabourContainer.module.css'
import baseClasses from '../../../../shared-components/shared-styles.module.css'
import CompleteLabourButton from '../Buttons/CompleteLabour'
import { useState } from 'react';

export function CompleteLabour({activeContraction}: {activeContraction: boolean}) {
    const [labourNotes, setLabourNotes] = useState("");
    return (
        <div className={baseClasses.root}>
        <div className={baseClasses.header}>
          <Title fz="xl" className={baseClasses.title}>Complete Your Labour</Title>
        </div>
        <div className={baseClasses.body}>
          <Stack align='stretch' justify='center' gap='md'>
            <Textarea
                radius="lg"
                label="Your closing note"
                description="Share a closing note for your labour with your subscribers."
                classNames={
                    {
                        label: classes.labourNotesLabel,
                        description: classes.labourNotesDescription
                    }
                }
                onChange={(event) => setLabourNotes(event.currentTarget.value)}
            />
            <CompleteLabourButton disabled={!!activeContraction} labourNotes={labourNotes}/>
          </Stack>
        </div>
      </div>
    )

}