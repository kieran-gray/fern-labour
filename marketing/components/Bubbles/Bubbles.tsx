import classes from './Bubbles.module.css'

export const Bubbles = () => {
    return (
    <div className={classes.background}>
        <div className={classes.bubble}></div>
        <div className={classes.bubble}></div>
        <div className={classes.bubble}></div>
        <div className={classes.bubble}></div>
      </div>
    )
}