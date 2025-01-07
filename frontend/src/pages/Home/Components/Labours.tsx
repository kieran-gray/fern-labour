import { Badge, Button, Space, Text } from '@mantine/core';
import baseClasses from '../../../shared-components/shared-styles.module.css';
import { BirthingPersonDTO } from '../../../client';
import { useNavigate } from 'react-router-dom';
import { LabourStatistics } from '../../../shared-components/LabourStatistics/LabourStatistics';


export default function Labours({ birthingPerson }: { birthingPerson: BirthingPersonDTO }) {
  const navigate = useNavigate();
  const labours = birthingPerson.labours.map((labour) => (
    <div key={labour.id} className={baseClasses.body} >
      <div className={baseClasses.flexRowNoBP}>
        <Text className={baseClasses.text}>{new Date(labour.start_time).toDateString()}</Text>
        <Badge size='lg' pl={40} pr={40} mb={20} variant="light">{labour.current_phase}</Badge>
      </div>
      <LabourStatistics labour={labour} />
      <Space h={"sm"} />
      {labour.end_time && <Text className={baseClasses.text}>Closing Note: {labour.notes}</Text>}
      <div className={baseClasses.flexRowEndNoBP}>
        {!labour.end_time && <Button color="var(--mantine-color-pink-4)" pl={35} pr={35} radius="lg" variant="filled" onClick={() => navigate("/labour")}>Resume</Button>}
      </div>
    </div>

  ));
  if (birthingPerson.labours.length > 0) {
    return (
        <div className={baseClasses.flexRow}>
          {labours}
        </div>
    )
  } else {
    return (
      <div className={baseClasses.body}>
        <Text className={baseClasses.text}>Current and past labours will show here</Text>
      </div>
    )
  }
}
