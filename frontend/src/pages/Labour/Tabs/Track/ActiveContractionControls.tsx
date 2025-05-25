import { RefObject, useEffect, useState } from 'react';
import { ContractionDTO } from '@clients/labour_service/types.gen.ts';
import { Slider, Space, Text } from '@mantine/core';
import EndContractionButton from './EndContractionButton.tsx';
import Stopwatch, { StopwatchHandle } from './Stopwatch/Stopwatch.tsx';
import classes from './Contractions.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export function ActiveContractionControls({
  stopwatchRef,
  activeContraction,
  disabled,
}: {
  stopwatchRef: RefObject<StopwatchHandle>;
  activeContraction: ContractionDTO;
  disabled: boolean;
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
      <div className={baseClasses.flexRowNoBP} style={{ justifyContent: 'center' }}>
        {stopwatch}
      </div>
      <Space h="lg" />
      <Text ta="center" className={baseClasses.minorText}>
        Your contraction intensity
      </Text>
      <Slider
        classNames={{
          root: classes.slider,
          markLabel: classes.markLabel,
          track: classes.track,
        }}
        color="var(--mantine-primary-color-4)"
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
      <EndContractionButton
        intensity={intensity}
        activeContraction={activeContraction}
        disabled={disabled}
      />
    </div>
  );
}
