import { useState } from 'react';
import { LabourDTO } from '@clients/labour_service/index.ts';
import { IconChevronDown, IconChevronUp } from '@tabler/icons-react';
import { ActionIcon } from '@mantine/core';
import { ContractionControls } from './ContractionControls.tsx';
import classes from './FloatingContractionControls.module.css';

interface FloatingContractionControlsProps {
  labour: LabourDTO;
  activeTab: string | null;
  onToggle?: (isExpanded: boolean) => void;
}

export function FloatingContractionControls({
  labour,
  activeTab,
  onToggle,
}: FloatingContractionControlsProps) {
  const [isExpanded, setIsExpanded] = useState(true);
  const activeContraction = labour.contractions.find((contraction) => contraction.is_active);
  const completed = labour.end_time !== null;

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
          <ContractionControls labour={labour} />
        </div>
      )}
    </div>
  );
}
