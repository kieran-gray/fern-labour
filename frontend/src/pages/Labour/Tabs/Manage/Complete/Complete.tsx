import { useState } from 'react';
import { IconArrowLeft, IconPencil } from '@tabler/icons-react';
import { Button, Image, Text, Textarea, Title, Tooltip } from '@mantine/core';
import image from './celebrate.svg';
import CompleteLabourButton from './CompleteLabourButton';
import baseClasses from '../../../../../shared-components/shared-styles.module.css';
import classes from './Complete.module.css';

export default function Complete({
  activeContraction,
  setActiveTab,
  paidFeaturesEnabled,
}: {
  activeContraction: boolean;
  setActiveTab: Function;
  paidFeaturesEnabled: boolean;
}) {
  const [labourNotes, setLabourNotes] = useState('');
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <div className={baseClasses.content}>
            <Title order={1} visibleFrom="sm">
              Complete your labour
            </Title>
            <Title order={2} hiddenFrom="sm">
              Complete your labour
            </Title>
            <div className={baseClasses.flexRow} style={{ flexWrap: 'nowrap' }}>
              <div className={baseClasses.flexColumn}>
                <Text c="var(--mantine-color-gray-7)" mt="sm" mb="sm" size="md">
                  If you want to, you can add a note below before completing your labour which will
                  be shared with all of your subscribers.
                  <br />
                  <br />
                  You could use it to introduce the new addition to your family, or just to let
                  everyone know you are OK.
                </Text>
                <div className={classes.imageFlexRow}>
                  <Image src={image} className={classes.smallImage} />
                </div>
              </div>
              <Image src={image} className={classes.image} style={{ flexGrow: 1 }} />
            </div>
            <div className={baseClasses.flexColumn}>
              <Tooltip
                label="Paid feature"
                offset={5}
                radius="xl"
                position="bottom"
                withArrow
                transitionProps={{ duration: 100, transition: 'slide-down' }}
                disabled={paidFeaturesEnabled}
              >
                <Textarea
                  rightSection={<IconPencil size={18} stroke={1.5} />}
                  radius="lg"
                  size="md"
                  placeholder="Your closing note"
                  classNames={{
                    label: classes.labourNotesLabel,
                  }}
                  onChange={(event) => setLabourNotes(event.currentTarget.value)}
                  disabled={!paidFeaturesEnabled}
                />
              </Tooltip>

              <div className={baseClasses.flexRow} style={{ marginTop: '20px' }}>
                <Button
                  color="var(--mantine-color-pink-4)"
                  leftSection={<IconArrowLeft size={18} stroke={1.5} />}
                  variant="light"
                  radius="xl"
                  size="md"
                  h={48}
                  className={classes.backButton}
                  onClick={() => setActiveTab('details')}
                  type="submit"
                >
                  Go back to labour
                </Button>
                <CompleteLabourButton disabled={!!activeContraction} labourNotes={labourNotes} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
