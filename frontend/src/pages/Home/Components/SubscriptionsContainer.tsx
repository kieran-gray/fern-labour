import baseClasses from '../../../shared-components/shared-styles.module.css';
import Subscriptions from './Subscriptions';


export default function SubscriptionsContainer() {
    return (
      <div className={baseClasses.root}>
        <div className={baseClasses.header}>
          <div className={baseClasses.title}>Your subscriptions</div>
        </div>
        <div className={baseClasses.flexRow}>
          <Subscriptions />
        </div>
      </div>
    )
}