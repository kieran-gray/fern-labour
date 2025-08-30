import { useRef } from 'react';
import { ContractionDTO, LabourDTO } from '@clients/labour_service/index.ts';
import { ActiveContractionControls } from './ActiveContractionControls.tsx';
import StartContractionButton from './StartContractionButton.tsx';
import { StopwatchHandle } from './Stopwatch/Stopwatch.tsx';

interface ContractionControlsProps {
  labour: LabourDTO;
}

export function ContractionControls({ labour }: ContractionControlsProps) {
  const stopwatchRef = useRef<StopwatchHandle>(null);

  const activeContraction = labour.contractions.find((contraction) => contraction.is_active);
  const completed = labour.end_time !== null;

  const anyPlaceholderContractions = (contractions: ContractionDTO[]) => {
    return contractions.some((contraction) => contraction.id === 'placeholder');
  };
  const containsPlaceholderContractions = anyPlaceholderContractions(labour.contractions);

  // Don't show controls if labour is completed
  if (completed) {
    return null;
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
      <div style={{ width: '100%', maxWidth: '600px' }}>
        {activeContraction ? (
          <ActiveContractionControls
            stopwatchRef={stopwatchRef}
            activeContraction={activeContraction}
            disabled={containsPlaceholderContractions}
          />
        ) : (
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            <StartContractionButton stopwatchRef={stopwatchRef} />
          </div>
        )}
      </div>
    </div>
  );
}
