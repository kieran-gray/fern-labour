import { useState } from 'react';
import { ContractionReadModel } from '@base/clients/labour_service/types';
import { IconChevronDown, IconChevronUp } from '@tabler/icons-react';
import { ActionIcon } from '@mantine/core';
import { ContractionControls } from './ContractionControls';
import classes from './FloatingContractionControls.module.css';

interface FloatingContractionControlsProps {
  labourCompleted: boolean;
  activeContraction: ContractionReadModel | undefined;
  activeTab: string | null;
  onToggle?: (isExpanded: boolean) => void;
}

export function FloatingContractionControls({
  labourCompleted,
  activeContraction,
  activeTab,
  onToggle,
}: FloatingContractionControlsProps) {
  const [isExpanded, setIsExpanded] = useState(true);

  // Only show on track tab and when labour is not completed
  if (activeTab !== 'track' || labourCompleted) {
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
          <ContractionControls
            labourCompleted={labourCompleted}
            activeContraction={activeContraction}
          />
        </div>
      )}
    </div>
  );
}
