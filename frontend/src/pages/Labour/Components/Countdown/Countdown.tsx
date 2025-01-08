import { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import classes from './Countdown.module.css'

export interface CountdownHandle {
  start: () => void;
  stop: () => void;
  reset: () => void;
  set: (seconds: number) => void;
  seconds: number;
  isRunning: boolean;
}

export const Countdown = forwardRef<CountdownHandle>((_, ref) => {
  const [seconds, setSeconds] = useState(0);
  const [isRunning, setIsRunning] = useState(true);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;
    
    if (isRunning) {
      intervalId = setInterval(() => {
        setSeconds(prev => prev - 1);
      }, 1000);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [isRunning]);

  const formatTime = (totalSeconds: number): string => {
    return `${totalSeconds.toString().padStart(2, '0')}`;
  };

  useImperativeHandle(ref, () => ({
    start: () => {
      setIsRunning(true)
    },
    stop: () => setIsRunning(false),
    reset: () => setIsRunning(false),
    set: (seconds) => {setSeconds(seconds)},
    seconds,
    isRunning
  }));

  return (
    <div>
      <div className={classes.counter}>{formatTime(seconds)}</div>
    </div>
  );
});

export default Countdown;