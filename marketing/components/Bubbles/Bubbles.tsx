import classes from './Bubbles.module.css';

export const Bubbles = () => {
  return (
    <div className={classes.background}>
      <div className={classes.bubble} />
      <div className={classes.bubble} />
      <div className={classes.bubble} />
      <div className={classes.bubble} />
    </div>
  );
};
