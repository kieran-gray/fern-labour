import { useState } from 'react';
import { LabourDTO } from '@clients/labour_service/index.ts';
import { IconChevronDown, IconChevronUp } from '@tabler/icons-react';
import { ActionIcon } from '@mantine/core';
import { LabourUpdateControls } from './LabourUpdateControls.tsx';
import classes from './FloatingLabourUpdateControls.module.css';

interface FloatingLabourUpdateControlsProps {
  labour: LabourDTO;
  activeTab: string | null;
  onToggle?: (isExpanded: boolean) => void;
}

export function FloatingLabourUpdateControls({
  labour,
  activeTab,
  onToggle,
}: FloatingLabourUpdateControlsProps) {
  const [isExpanded, setIsExpanded] = useState(true);
  const completed = labour.end_time !== null;

  // Only show on updates tab and when labour is not completed
  if (activeTab !== 'updates' || completed) {
    return null;
  }

  const handleToggle = () => {
    const newExpanded = !isExpanded;
    setIsExpanded(newExpanded);
    onToggle?.(newExpanded);
  };

  return (
    <div className={`${classes.floatingControls} ${!isExpanded ? classes.collapsed : ''}`}>
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
          <LabourUpdateControls />
        </div>
      )}
    </div>
  );
}
