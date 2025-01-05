import { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import classes from './Stopwatch.module.css'

export interface StopwatchHandle {
  start: () => void;
  stop: () => void;
  reset: () => void;
  set: (seconds: number) => void;
  seconds: number;
  isRunning: boolean;
}

const Stopwatch = forwardRef<StopwatchHandle>((_, ref) => {
  const [seconds, setSeconds] = useState(0);
  const [isRunning, setIsRunning] = useState(true);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;
    
    if (isRunning) {
      intervalId = setInterval(() => {
        setSeconds(prev => prev + 1);
      }, 1000);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [isRunning]);

  const formatTime = (totalSeconds: number): string => {
    const minutes = Math.floor(totalSeconds / 60);
    const remainingSeconds = totalSeconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  useImperativeHandle(ref, () => ({
    start: () => setIsRunning(true),
    stop: () => setIsRunning(false),
    reset: () => {
      setIsRunning(false);
      setSeconds(0);
    },
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

export default Stopwatch;