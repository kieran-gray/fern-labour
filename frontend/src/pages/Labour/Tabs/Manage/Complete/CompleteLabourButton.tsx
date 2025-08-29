import { useState } from 'react';
import { GenericConfirmModal } from '@base/shared-components/GenericConfirmModal/GenericConfirmModal';
import { useCompleteLabour } from '@shared/hooks';
import { IconConfetti } from '@tabler/icons-react';
import { Button, Tooltip } from '@mantine/core';
import { useLabour } from '@base/pages/Labour/LabourContext';
import { useNavigate } from 'react-router-dom';

export default function CompleteLabourButton({
  labourNotes,
  disabled,
}: {
  labourNotes: string;
  disabled: boolean;
}) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const completeLabourMutation = useCompleteLabour();
  const navigate = useNavigate();
  const { setLabourId } = useLabour();

  const handleCompleteLabour = (labourNotes: string) => {
    completeLabourMutation.mutate(labourNotes);
    setLabourId(null);
    navigate('/completed');
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
          loading={completeLabourMutation.isPending}
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
