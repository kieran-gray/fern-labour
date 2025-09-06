import { useEffect, useMemo, useRef, useState } from 'react';
import { ContractionDTO } from '@clients/labour_service';
import { formatTimeMilliseconds, formatTimeSeconds, getTimeSinceLastStarted } from '@shared/utils';
import { IconActivityHeartbeat, IconNotes } from '@tabler/icons-react';
import { Group, ScrollArea, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { EditContractionModal } from './EditContractionModal';
import classes from './ContractionTimelineCustom.module.css';

const DOTTED_LINE_FREQUENCY_GAP = 1800000; // 30 minutes

export interface ContractionData {
  contractionId: string;
  startTime: string;
  endTime: string;
  intensity: number | null;
}

type Section = { key: string; label: string; items: ContractionDTO[] };

export default function ContractionTimelineCustom({
  contractions,
  completed,
}: {
  contractions: ContractionDTO[];
  completed: boolean;
}) {
  const viewport = useRef<HTMLDivElement>(null);
  const [opened, { open, close }] = useDisclosure(false);
  const [modalData, setModalData] = useState<ContractionData | null>(null);

  const isFinished = (c: ContractionDTO) => c.start_time !== c.end_time;
  const gaps = useMemo(() => getTimeSinceLastStarted(contractions), [contractions]);

  useEffect(() => {
    if (viewport.current) {
      viewport.current.scrollTo({ top: viewport.current.scrollHeight, behavior: 'auto' });
    }
  }, [contractions]);

  const formatClock = (iso: string) =>
    new Date(iso).toLocaleTimeString(navigator.language, { hour: '2-digit', minute: '2-digit' });

  const handleClick = (c: ContractionDTO) => {
    if (!completed && isFinished(c)) {
      setModalData({
        contractionId: c.id,
        startTime: c.start_time,
        endTime: c.end_time,
        intensity: c.intensity,
      });
      open();
    }
  };

  const sections: Section[] = useMemo(() => {
    const map = new Map<string, ContractionDTO[]>();
    for (const c of contractions) {
      const d = new Date(c.start_time);
      const key = `${d.getFullYear()}-${(d.getMonth() + 1).toString().padStart(2, '0')}-${d
        .getDate()
        .toString()
        .padStart(2, '0')}`;
      if (!map.has(key)) {
        map.set(key, []);
      }
      map.get(key)!.push(c);
    }
    return Array.from(map.entries()).map(([key, items]) => ({
      key,
      label: new Date(items[0].start_time).toLocaleDateString(navigator.language, {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
      }),
      items,
    }));
  }, [contractions]);

  const renderItem = (c: ContractionDTO, idx: number, arr: ContractionDTO[]) => {
    const finished = isFinished(c);
    const nextGap = gaps[c.id]?.next ?? 0;
    const clickable = finished && !completed;

    const node = (
      <div key={`${c.id}-node`} className={classes.gridRow}>
        <div className={classes.leftColumn}>
          <div className={classes.durationDisplay}>
            {finished ? (
              <Text size="lg" fw={600} className={classes.durationText}>
                {formatTimeSeconds(c.duration)}
              </Text>
            ) : (
              <Text size="lg" fw={600} className={classes.ongoingText}>
                Ongoing
              </Text>
            )}
          </div>
          <div className={classes.timeDisplay}>
            <Text size="sm" className={classes.timeText}>
              {formatClock(c.start_time)}
            </Text>
          </div>
        </div>
        <div className={classes.centerColumn}>
          <div
            className={`${classes.railCell} ${
              nextGap > DOTTED_LINE_FREQUENCY_GAP ? classes.longGap : ''
            }`}
            aria-hidden
          >
            <div
              className={finished ? classes.bullet : `${classes.bullet} ${classes.bulletActive}`}
              style={{ background: 'var(--mantine-primary-color-4)' }}
              onClick={() => handleClick(c)}
              role={clickable ? 'button' : undefined}
              aria-label={
                finished
                  ? `Contraction at ${formatClock(c.start_time)}, intensity ${c.intensity ?? 0}`
                  : `Ongoing contraction started at ${formatClock(c.start_time)}`
              }
            >
              {finished ? (c.intensity ?? 0) : <IconActivityHeartbeat size={28} color="white" />}
            </div>
          </div>
        </div>
        <div className={classes.rightColumn}>
          {c.notes && (
            <Group gap={6} wrap="nowrap" className={classes.noteRow}>
              <IconNotes size={16} color="var(--mantine-color-gray-6)" />
              <Text size="sm">{c.notes}</Text>
            </Group>
          )}
        </div>
      </div>
    );

    const connector = idx < arr.length - 1 && nextGap > 0 && (
      <div key={`${c.id}-connector`} className={classes.connectorRow}>
        <div className={classes.connectorLeft}>{/* Empty space for left column */}</div>
        <div className={classes.connectorCenter}>{/* Timeline continues through center */}</div>
        <div className={classes.connectorRight}>
          <div className={classes.frequencyDisplay}>
            <Text size="sm" fw={500} className={classes.frequencyText}>
              {formatTimeMilliseconds(nextGap)}
            </Text>
          </div>
        </div>
      </div>
    );

    return connector ? [node, connector] : [node];
  };

  return (
    <div className={classes.timelineContainer}>
      {modalData && !completed && (
        <EditContractionModal contractionData={modalData} opened={opened} close={close} />
      )}
      {sections.length > 0 && (
        <div className={classes.headerRow}>
          <div className={classes.headerLeft}>
            <Text size="sm" fw={600} c="dimmed">
              Duration
            </Text>
          </div>
          <div className={classes.headerCenter}>
            {/* Timeline column - no header text needed */}
          </div>
          <div className={classes.headerRight}>
            <Text size="sm" fw={600} c="dimmed">
              Frequency
            </Text>
          </div>
        </div>
      )}
      <ScrollArea.Autosize mah="calc(100dvh - 400px)" viewportRef={viewport} w="100%">
        <div className={classes.root}>
          {sections.length === 0 && <Text ta="center">No contractions recorded yet</Text>}
          {sections.map((section) => (
            <div key={section.key} className={classes.daySection}>
              <div className={classes.dayHeader}>
                <div>
                  <Text size="sm" className={classes.dayTitle}>
                    {section.label}
                  </Text>
                  <div className={classes.dayRule} />
                </div>
              </div>
              {section.items.flatMap((c, i, arr) => renderItem(c, i, arr))}
            </div>
          ))}
        </div>
      </ScrollArea.Autosize>
    </div>
  );
}
