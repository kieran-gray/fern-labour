import { RefObject, useEffect, useState } from 'react';
import { Slider, Space, Text } from '@mantine/core';
import { ContractionDTO } from '../../../../client/types.gen.ts';
import Stopwatch, { StopwatchHandle } from '../Stopwatch/Stopwatch.tsx';
import EndContractionButton from './EndContractionButton.tsx';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './Contractions.module.css';

export function ActiveContractionControls({
  stopwatchRef,
  activeContraction,
}: {
  stopwatchRef: RefObject<StopwatchHandle>;
  activeContraction: ContractionDTO;
}) {
  const [intensity, setIntensity] = useState(5);
  const stopwatch = <Stopwatch ref={stopwatchRef} />;

  useEffect(() => {
    const startTime = new Date(activeContraction.start_time).getTime();
    const seconds = stopwatchRef.current?.seconds || 0;
    const secondsElapsed = Math.round((Date.now() - startTime) / 1000);
    if (Math.abs(secondsElapsed - seconds) > 1) {
      stopwatchRef.current?.set(secondsElapsed);
    }
  }, [stopwatchRef]);

  return (
    <div className={classes.controlsBackground}>
      {stopwatch}
      <Space h="lg" />
      <Text className={baseClasses.minorText}>
        Set your contraction intensity before ending the contraction
      </Text>
      <Slider
        classNames={{
          root: classes.slider,
          markLabel: classes.markLabel,
          track: classes.track,
        }}
        color="var(--mantine-color-pink-4)"
        size="xl"
        radius="lg"
        min={0}
        max={10}
        step={1}
        defaultValue={5}
        onChange={setIntensity}
        marks={[
          { value: 0, label: '0' },
          { value: 5, label: 5 },
          { value: 10, label: 10 },
        ]}
      />
      <Space h="xl" />
      <EndContractionButton intensity={intensity} />
    </div>
  );
}
