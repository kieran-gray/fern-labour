import { NotFoundError } from '@base/Errors.tsx';
import { ApiError } from '@clients/labour_service/index.ts';
import { AppShell } from '@shared/AppShell';
import { ErrorContainer } from '@shared/ErrorContainer/ErrorContainer.tsx';
import { useActiveLabour } from '@shared/hooks/index.ts';
import { PageLoading } from '@shared/PageLoading/PageLoading.tsx';
import Plan from './Components/Plan/Plan.tsx';
import baseClasses from '@shared/shared-styles.module.css';

export const OnboardingPage = () => {
  const { isPending, isError, data, error } = useActiveLabour();

  if (isPending) {
    return <PageLoading />;
  } else if (isError) {
    if (error instanceof ApiError && error.status === 404) {
      // Continue with undefined labour for new users
      // No need to return here
    } else {
      return <ErrorContainer message="Failed to load labour details. Please try again later." />;
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
                <Plan labour={labour} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
};
