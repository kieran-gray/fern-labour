import { useState } from 'react';
import {
  IconArrowLeft,
  IconArrowRight,
  IconCurrencyPound,
  IconPencil,
  IconSend,
} from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { Button, Group, Space, Stepper } from '@mantine/core';
import { ApiError, OpenAPI } from '../../client/index.ts';
import { LabourService } from '../../client/sdk.gen.ts';
import { LabourDTO } from '../../client/types.gen.ts';
import { NotFoundError } from '../../Errors.tsx';
import { AppShell } from '../../shared-components/AppShell.tsx';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading.tsx';
import { useLabour } from '../Labour/LabourContext.tsx';
import { InviteContainer } from '../Labour/Tabs/Invites/InviteContainer/InviteContainer.tsx';
import { ShareContainer } from '../Labour/Tabs/Invites/ShareContainer/ShareContainer.tsx';
import Plan from './Components/Plan/Plan.tsx';
import { Pricing01 } from './Components/Pricing/Pricing.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';
import classes from './Onboarding.module.css';

export const OnboardingPage = () => {
  const auth = useAuth();
  const navigate = useNavigate();
  const { labourId } = useLabour();
  let labour: LabourDTO | undefined = undefined;
  const [active, setActive] = useState(0);
  const [highestStepVisited, setHighestStepVisited] = useState(active);

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const handleStepChange = (nextStep: number) => {
    const isOutOfBounds = nextStep > 3 || nextStep < 0;
    if (isOutOfBounds) {
      return;
    }
    if (nextStep === 3) {
      navigate('/');
    }
    setActive(nextStep);
    setHighestStepVisited((hSC) => Math.max(hSC, nextStep));
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['labour', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await LabourService.getActiveLabourApiV1LabourActiveGet();
        return response.labour;
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) {
          throw new NotFoundError();
        }
        throw new Error('Failed to load labour. Please try again later.');
      }
    },
    retry: 0,
  });

  if (isPending) {
    return <PageLoading />;
  } else if (isError) {
    if (error instanceof NotFoundError) {
      labour = undefined;
    } else {
      return <ErrorContainer message={error.message} />;
    }
  } else {
    labour = data;
  }

  const nextStepEnabled = labour?.payment_plan != null;

  // Allow the user to freely go back and forth between visited steps.
  const shouldAllowSelectStep = (step: number) => {
    const visited = highestStepVisited >= step && active !== step;
    if (step === 1 && labourId != null && labourId !== '') {
      return true;
    }
    if (step === 2 && labour?.payment_plan != null) {
      return true;
    }
    return visited;
  };

  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn} style={{ flexGrow: 1 }}>
        <div className={baseClasses.root} style={{ width: '100%' }}>
          <div className={baseClasses.body}>
            <div className={baseClasses.inner}>
              <div className={baseClasses.flexColumn} style={{ flexGrow: 1, width: '100%' }}>
                <Stepper
                  active={active}
                  onStepClick={setActive}
                  classNames={{
                    step: classes.stepperStep,
                    stepLabel: classes.stepperStepLabel,
                    stepDescription: classes.stepperStepDescription,
                    content: classes.stepperContent,
                    stepIcon: classes.stepperStepIcon,
                  }}
                >
                  <Stepper.Step
                    icon={<IconPencil size={18} />}
                    label="Step 1"
                    description="Your Labour Details"
                    allowStepSelect={shouldAllowSelectStep(0)}
                  >
                    <Plan
                      labour={labour}
                      setActiveTab={() => {
                        handleStepChange(active + 1);
                      }}
                    />
                  </Stepper.Step>
                  <Stepper.Step
                    icon={<IconCurrencyPound size={18} />}
                    label="Step 2"
                    description="Pay"
                    allowStepSelect={shouldAllowSelectStep(1)}
                  >
                    <div style={{ display: 'flex', flexGrow: 1 }}>
                      <Pricing01 labour={labour} />
                    </div>
                  </Stepper.Step>
                  <Stepper.Step
                    icon={<IconSend size={18} />}
                    label="Step 3"
                    description="Invite Loved Ones"
                    allowStepSelect={shouldAllowSelectStep(2)}
                  >
                    <InviteContainer />
                    <Space h="xl" />
                    <ShareContainer />
                  </Stepper.Step>
                </Stepper>
                {active !== 0 && (
                  <Group justify="space-between" mt="xl">
                    <Button
                      variant="light"
                      radius="xl"
                      size="lg"
                      leftSection={<IconArrowLeft size={18} />}
                      onClick={() => handleStepChange(active - 1)}
                      visibleFrom="sm"
                    >
                      {active === 1 ? 'Back to planning' : 'Back to payment'}
                    </Button>
                    <Button
                      variant="light"
                      radius="lg"
                      size="sm"
                      leftSection={<IconArrowLeft size={18} />}
                      onClick={() => handleStepChange(active - 1)}
                      hiddenFrom="sm"
                    >
                      {active === 1 ? 'Back to planning' : 'Back to payment'}
                    </Button>
                    <Button
                      radius="xl"
                      size="lg"
                      color="var(--mantine-color-pink-4)"
                      rightSection={<IconArrowRight size={18} />}
                      onClick={() => handleStepChange(active + 1)}
                      visibleFrom="sm"
                      disabled={!nextStepEnabled}
                    >
                      {active === 2 ? 'Go to app' : 'Next step'}
                    </Button>
                    <Button
                      radius="lg"
                      size="sm"
                      color="var(--mantine-color-pink-4)"
                      rightSection={<IconArrowRight size={18} />}
                      onClick={() => handleStepChange(active + 1)}
                      hiddenFrom="sm"
                      disabled={!nextStepEnabled}
                    >
                      {active === 2 ? 'Go to app' : 'Next step'}
                    </Button>
                  </Group>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
};
