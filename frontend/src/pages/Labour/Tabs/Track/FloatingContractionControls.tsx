import { RefObject, useState } from 'react';
import { ContractionDTO, LabourDTO } from '@clients/labour_service/index.ts';
import { IconChevronDown, IconChevronUp } from '@tabler/icons-react';
import { ActionIcon } from '@mantine/core';
import { ActiveContractionControls } from './ActiveContractionControls.tsx';
import StartContractionButton from './StartContractionButton.tsx';
import { StopwatchHandle } from './Stopwatch/Stopwatch.tsx';
import classes from './FloatingContractionControls.module.css';

interface FloatingContractionControlsProps {
  labour: LabourDTO;
  stopwatchRef: RefObject<StopwatchHandle>;
  activeTab: string | null;
  onToggle?: (isExpanded: boolean) => void;
}

export function FloatingContractionControls({
  labour,
  stopwatchRef,
  activeTab,
  onToggle,
}: FloatingContractionControlsProps) {
  const [isExpanded, setIsExpanded] = useState(true);
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

  const handleToggle = () => {
    const newExpanded = !isExpanded;
    setIsExpanded(newExpanded);
    onToggle?.(newExpanded);
  };

  return (
    <div
      className={`${classes.floatingControls} ${activeContraction ? classes.activeContraction : ''} ${!isExpanded ? classes.collapsed : ''}`}
    >
      <div className={classes.header}>
        <ActionIcon
          variant="subtle"
          size="sm"
          onClick={handleToggle}
          className={classes.toggleButton}
        >
          {isExpanded ? <IconChevronDown size={16} /> : <IconChevronUp size={16} />}
        </ActionIcon>
      </div>
      
      {isExpanded && (
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
      )}
    </div>
  );
}
