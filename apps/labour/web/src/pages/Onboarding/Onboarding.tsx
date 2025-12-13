import { NotFoundError } from '@base/lib/errors';
import { AppShell } from '@shared/AppShell';
import { useActiveLabour } from '@shared/hooks/index';
import { PageLoading } from '@shared/PageLoading/PageLoading';
import Plan from './Components/Plan/Plan';
import baseClasses from '@shared/shared-styles.module.css';

export const OnboardingPage = () => {
  const { isPending, isError, data, error } = useActiveLabour();

  if (isPending) {
    return <PageLoading />;
  }

  const labour = isError && error instanceof NotFoundError ? undefined : data;

  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
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
