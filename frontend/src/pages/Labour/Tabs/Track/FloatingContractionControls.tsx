import { RefObject } from 'react';
import { ContractionDTO, LabourDTO } from '@clients/labour_service/index.ts';
import { ActiveContractionControls } from './ActiveContractionControls.tsx';
import StartContractionButton from './StartContractionButton.tsx';
import { StopwatchHandle } from './Stopwatch/Stopwatch.tsx';
import classes from './FloatingContractionControls.module.css';

interface FloatingContractionControlsProps {
  labour: LabourDTO;
  stopwatchRef: RefObject<StopwatchHandle>;
  activeTab: string | null;
}

export function FloatingContractionControls({ 
  labour, 
  stopwatchRef, 
  activeTab 
}: FloatingContractionControlsProps) {
  const activeContraction = labour.contractions.find((contraction) => contraction.is_active);
  const completed = labour.end_time !== null;
  
  const anyPlaceholderContractions = (contractions: ContractionDTO[]) => {
    return contractions.some((contraction) => contraction.id === 'placeholder');
  };
  const containsPlaceholderContractions = anyPlaceholderContractions(labour.contractions);

  // Only show on track tab and when labour is not completed
  if (activeTab !== 'track' || completed) {
    return null;
  }

  return (
    <div className={`${classes.floatingControls} ${activeContraction ? classes.activeContraction : ''}`}>
      <div className={classes.controlsContent}>
        {activeContraction ? (
          <ActiveContractionControls
            stopwatchRef={stopwatchRef}
            activeContraction={activeContraction}
            disabled={containsPlaceholderContractions}
          />
        ) : (
          <StartContractionButton stopwatchRef={stopwatchRef} />
        )}
      </div>
    </div>
  );
}