import baseClasses from '../../../shared-components/shared-styles.module.css';
import { BirthingPersonDTO } from '../../../client';
import Labours from './Labours';


export default function LabourContainer({ birthingPerson }: { birthingPerson: BirthingPersonDTO }) {
    return (
      <div className={baseClasses.root}>
        <div className={baseClasses.header}>
          <div className={baseClasses.title}>Your Labours</div>
        </div>
        <div className={baseClasses.flexRow}>
          <Labours birthingPerson={birthingPerson} />
        </div>
      </div>
    )
}