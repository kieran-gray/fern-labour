import baseClasses from '../shared-styles.module.css';
import classes from './ErrorContainer.module.css';

export function ErrorContainer({ message }: { message: string }) {
  return (
    <div className={classes.container}>
      <div className={baseClasses.root}>
        <div className={baseClasses.header}>
          <div className={baseClasses.title}>We've hit a snag :(</div>
        </div>
        <div className={baseClasses.body}>
          <div className={baseClasses.text}>{message}</div>
        </div>
      </div>
    </div>
  );
}
