import { useState } from 'react';
import { GenericConfirmModal } from '@base/shared-components/GenericConfirmModal/GenericConfirmModal';
import { useCompleteLabour } from '@base/shared-components/hooks';
import { IconConfetti } from '@tabler/icons-react';
import { Button, Tooltip } from '@mantine/core';

export default function CompleteLabourButton({
  labourNotes,
  disabled,
}: {
  labourNotes: string;
  disabled: boolean;
}) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isMutating, setIsMutating] = useState(false);
  const completeLabourMutation = useCompleteLabour();

  const handleCompleteLabour = async (labourNotes: string) => {
    setIsMutating(true);
    try {
      await completeLabourMutation.mutateAsync(labourNotes);
    } finally {
      setIsMutating(false);
    }
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  const handleConfirm = () => {
    setIsModalOpen(false);
    handleCompleteLabour(labourNotes);
  };

  const icon = <IconConfetti size={25} />;

  if (disabled) {
    return (
      <Tooltip
        label="End your current contraction first"
        events={{ hover: true, focus: false, touch: true }}
      >
        <Button
          data-disabled
          leftSection={icon}
          size="lg"
          color="var(--mantine-color-pink-4)"
          radius="xl"
          variant="filled"
          loading={isMutating}
          onClick={(event) => event.preventDefault()}
        >
          Complete Labour
        </Button>
      </Tooltip>
    );
  }
  return (
    <>
      <Button
        leftSection={icon}
        size="lg"
        color="var(--mantine-color-pink-4)"
        radius="xl"
        variant="filled"
        onClick={() => setIsModalOpen(true)}
      >
        Complete Labour
      </Button>
      <GenericConfirmModal
        isOpen={isModalOpen}
        title="Complete your labour?"
        confirmText="Yes"
        message="Are you sure you want to complete your current labour?"
        onConfirm={handleConfirm}
        onCancel={handleCancel}
        isDangerous
      />
    </>
  );
}
