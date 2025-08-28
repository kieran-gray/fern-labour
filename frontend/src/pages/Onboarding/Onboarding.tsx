import { NotFoundError } from '@base/Errors.tsx';
import { ApiError } from '@clients/labour_service/index.ts';
import { LabourQueriesService } from '@clients/labour_service/sdk.gen.ts';
import { useLabour } from '@labour/LabourContext.tsx';
import { AppShell } from '@shared/AppShell';
import { ErrorContainer } from '@shared/ErrorContainer/ErrorContainer.tsx';
import { useApiAuth } from '@shared/hooks/useApiAuth';
import { PageLoading } from '@shared/PageLoading/PageLoading.tsx';
import { useQuery } from '@tanstack/react-query';
import { Stepper } from '@mantine/core';
import Plan from './Components/Plan/Plan.tsx';
import classes from './Onboarding.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export const OnboardingPage = () => {
  const { user } = useApiAuth();
  const { setLabourId } = useLabour();

  const { isPending, isError, data, error } = useQuery({
    queryKey: ['labour', user?.profile.sub],
    queryFn: async () => {
      try {
        const response = await LabourQueriesService.getActiveLabour();
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

  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn} style={{ flexGrow: 1 }}>
        <div className={baseClasses.root} style={{ width: '100%' }}>
          <div className={baseClasses.body}>
            <div className={baseClasses.inner}>
              <div className={baseClasses.flexColumn} style={{ flexGrow: 1, width: '100%' }}>
                <Stepper
                  active={0}
                  classNames={{
                    step: classes.stepperStep,
                    stepLabel: classes.stepperStepLabel,
                    stepDescription: classes.stepperStepDescription,
                    stepIcon: classes.stepperStepIcon,
                  }}
                >
                  <Stepper.Step>
                    <Plan labour={labour} />
                  </Stepper.Step>
                </Stepper>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
};
