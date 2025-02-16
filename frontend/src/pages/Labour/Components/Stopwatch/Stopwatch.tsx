import { forwardRef, useEffect, useImperativeHandle, useState } from 'react';
import classes from './Stopwatch.module.css';

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
  const [startTime, setStartTime] = useState<number | null>(null);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    if (isRunning) {
      if (!startTime) {
        setStartTime(Date.now() - seconds * 1000);
      }

      intervalId = setInterval(() => {
        const now = Date.now();
        const expectedSeconds = Math.floor((now - (startTime || now)) / 1000);
        if (Math.abs(expectedSeconds - seconds) >= 1) {
          setSeconds(expectedSeconds);
        } else {
          setSeconds((prev) => prev + 1);
        }
      }, 1000);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [isRunning, startTime, seconds]);

  const formatTime = (totalSeconds: number): string => {
    const minutes = Math.floor(totalSeconds / 60);
    const remainingSeconds = totalSeconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  useImperativeHandle(ref, () => ({
    start: () => {
      setStartTime(Date.now() - seconds * 1000);
      setIsRunning(true);
    },
    stop: () => {
      setIsRunning(false);
      setStartTime(null);
    },
    reset: () => {
      setIsRunning(false);
      setSeconds(0);
      setStartTime(null);
    },
    set: (newSeconds) => {
      setSeconds(newSeconds);
      if (isRunning) {
        setStartTime(Date.now() - newSeconds * 1000);
      }
    },
    seconds,
    isRunning,
  }));

  return (
    <div>
      <div className={classes.counter}>{formatTime(seconds)}</div>
    </div>
  );
});

export default Stopwatch;
