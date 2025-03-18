import { useState } from 'react';
import {
  IconArrowLeft,
  IconArrowRight,
  IconCurrencyPound,
  IconPencil,
  IconReceipt,
} from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from 'react-oidc-context';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Button, Stepper } from '@mantine/core';
import { useWindowScroll } from '@mantine/hooks';
import { ApiError, OpenAPI } from '../../client/index.ts';
import { LabourService } from '../../client/sdk.gen.ts';
import { NotFoundError } from '../../Errors.tsx';
import { AppShell } from '../../shared-components/AppShell.tsx';
import { ErrorContainer } from '../../shared-components/ErrorContainer/ErrorContainer.tsx';
import { PageLoading } from '../../shared-components/PageLoading/PageLoading.tsx';
import { useLabour } from '../Labour/LabourContext.tsx';
import Plan from './Components/Plan/Plan.tsx';
import { Pricing01 } from './Components/Pricing/Pricing.tsx';
import { RecieptContainer } from './Components/Receipt/Receipt.tsx';
import baseClasses from '../../shared-components/shared-styles.module.css';
import classes from './Onboarding.module.css';

const stepOrder = ['plan', 'pay', 'receipt'];

export const OnboardingPage = () => {
  const auth = useAuth();
  const navigate = useNavigate();
  const { labourId, setLabourId } = useLabour();
  const [searchParams] = useSearchParams();
  const step = searchParams.get('step');
  const [active, setActive] = useState(step ? stepOrder.indexOf(step) : 0);
  const [highestStepVisited, setHighestStepVisited] = useState(active);
  const [_, scrollTo] = useWindowScroll();

  OpenAPI.TOKEN = async () => {
    return auth.user?.access_token || '';
  };

  const handleStepChange = (nextStep: number) => {
    if (nextStep < 0 || nextStep > 3) {
      return;
    }
    if (nextStep === 3) {
      navigate('/');
      return;
    }
    setActive(nextStep);
    scrollTo({ y: 0 });
    setHighestStepVisited((hSC) => Math.max(hSC, nextStep));
  };

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['labour', auth.user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await LabourService.getActiveLabourApiV1LabourActiveGet();
        setLabourId(response.labour.id);
        return response.labour;
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) {
          throw new NotFoundError();
        }
        throw new Error('Failed to load labour details. Please try again later.');
      }
    },
    retry: 1,
    refetchOnWindowFocus: false,
  });

  if (isPending) {
    return <PageLoading />;
  } else if (isError) {
    if (error instanceof NotFoundError) {
      // Continue with undefined labour for new users
      // No need to return here
    } else {
      return <ErrorContainer message={error.message} />;
    }
  }

  const labour = isError && error instanceof NotFoundError ? undefined : data;
  const nextStepEnabled = labour?.payment_plan != null;

  const shouldAllowSelectStep = (step: number) => {
    const visited = highestStepVisited >= step && active !== step;
    if (step === 1 && labourId != null && labourId !== '') {
      return true;
    }
    if (step === 2 && labour?.payment_plan != null && labour.payment_plan !== 'solo') {
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
                    <Plan labour={labour} gotoNextStep={() => handleStepChange(active + 1)} />
                  </Stepper.Step>
                  <Stepper.Step
                    icon={<IconCurrencyPound size={18} />}
                    label="Step 2"
                    description="Payment Options"
                    allowStepSelect={shouldAllowSelectStep(1)}
                  >
                    <div style={{ display: 'flex', flexGrow: 1 }}>
                      <Pricing01 labour={labour} />
                    </div>
                  </Stepper.Step>
                  <Stepper.Step
                    icon={<IconReceipt size={18} />}
                    label="Step 3"
                    description="Thank you"
                    allowStepSelect={shouldAllowSelectStep(2)}
                    onClick={() => handleStepChange(active + 1)}
                  >
                    <div style={{ display: 'flex', flexGrow: 1 }}>
                      <RecieptContainer />
                    </div>
                  </Stepper.Step>
                </Stepper>
                {active !== 0 && (
                  <div className={classes.submitRow}>
                    <Button
                      variant="light"
                      radius="xl"
                      size="md"
                      h={48}
                      leftSection={<IconArrowLeft size={18} />}
                      onClick={() => handleStepChange(active - 1)}
                    >
                      Back to planning
                    </Button>
                    <Button
                      radius="xl"
                      size="md"
                      h={48}
                      color="var(--mantine-color-pink-4)"
                      rightSection={<IconArrowRight size={18} />}
                      onClick={() => handleStepChange(active + 1)}
                      disabled={!nextStepEnabled}
                      className={classes.backButton}
                    >
                      {nextStepEnabled ? 'Go to app' : 'Please select a plan'}
                    </Button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
};
