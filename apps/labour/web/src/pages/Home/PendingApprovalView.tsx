import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { IconX } from '@tabler/icons-react';
import { Button } from '@mantine/core';
import baseClasses from '@shared/shared-styles.module.css';

interface PendingApprovalViewProps {
  onCancel: () => void;
}

export function PendingApprovalView({ onCancel }: PendingApprovalViewProps) {
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner}>
          <div className={baseClasses.content}>
            <ResponsiveTitle title="Awaiting Approval" />
            <ResponsiveDescription
              description="Your subscription request has been sent. The mother will need to approve your request before you can view their labour updates. You'll be notified once you're approved."
              marginTop={10}
            />
            <Button
              variant="light"
              color="red"
              radius="xl"
              size="md"
              mt="xl"
              leftSection={<IconX size={18} />}
              onClick={onCancel}
            >
              Cancel Request
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
