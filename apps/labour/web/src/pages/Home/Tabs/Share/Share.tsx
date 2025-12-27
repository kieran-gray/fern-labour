import { Space } from '@mantine/core';
import { InviteByEmail } from './InviteByEmail/InviteByEmail';
import { ShareLabour } from './ShareLabour/ShareLabour';
import baseClasses from '@shared/shared-styles.module.css';

export function Share() {
  return (
    <>
      <div className={baseClasses.root}>
        <div className={baseClasses.body}>
          <ShareLabour />
        </div>
      </div>
      <Space h="xl" />
      <div className={baseClasses.root}>
        <div className={baseClasses.body}>
          <InviteByEmail />
        </div>
      </div>
    </>
  );
}
