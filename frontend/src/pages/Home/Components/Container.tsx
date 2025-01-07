import baseClasses from '../../../shared-components/shared-styles.module.css';
import Labours from './Labours';


export default function LabourContainer() {
    return (
      <div className={baseClasses.root}>
        <div className={baseClasses.header}>
          <div className={baseClasses.title}>Your Labours</div>
        </div>
        <div className={baseClasses.flexRow}>
          <Labours />
        </div>
      </div>
    )
}