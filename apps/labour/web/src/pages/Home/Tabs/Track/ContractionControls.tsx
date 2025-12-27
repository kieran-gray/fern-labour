import { useRef } from 'react';
import { ContractionReadModel } from '@base/clients/labour_service/types';
import { ActiveContractionControls } from './ActiveContractionControls';
import StartContractionButton from './StartContractionButton';
import { StopwatchHandle } from './Stopwatch/Stopwatch';

interface ContractionControlsProps {
  labourCompleted: boolean;
  activeContraction: ContractionReadModel | undefined;
}

export function ContractionControls({
  labourCompleted,
  activeContraction,
}: ContractionControlsProps) {
  const stopwatchRef = useRef<StopwatchHandle>(null);
  // Don't show controls if labour is completed
  if (labourCompleted) {
    return null;
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'center', width: '100%' }}>
      <div style={{ width: '100%', maxWidth: '600px' }}>
        {activeContraction ? (
          <ActiveContractionControls
            stopwatchRef={stopwatchRef}
            activeContraction={activeContraction}
            disabled={false}
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
