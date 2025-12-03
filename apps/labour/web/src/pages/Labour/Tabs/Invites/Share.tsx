import { Space } from '@mantine/core';
import { InviteContainer } from './InviteContainer/InviteContainer';
import { ShareContainer } from './ShareContainer/ShareContainer';
import baseClasses from '@shared/shared-styles.module.css';

export function Share() {
  return (
    <>
      <div className={baseClasses.root}>
        <div className={baseClasses.body}>
          <ShareContainer />
        </div>
      </div>
      <Space h="xl" />
      <div className={baseClasses.root}>
        <div className={baseClasses.body}>
          <InviteContainer />
        </div>
      </div>
    </>
  );
}
