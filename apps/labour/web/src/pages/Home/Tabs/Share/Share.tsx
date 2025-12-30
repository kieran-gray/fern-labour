import { Space } from '@mantine/core';
import { InviteByEmail } from './InviteByEmail';
import { ShareLabour } from './ShareLabour';
import baseClasses from '@components/shared-styles.module.css';

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
