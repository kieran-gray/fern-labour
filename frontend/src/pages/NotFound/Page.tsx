import { AppShell } from '@shared/AppShell';
import { NotFoundImage } from './Components/Image/Image';
import baseClasses from '@shared/shared-styles.module.css';

export const NotFoundPage: React.FC = () => {
  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <NotFoundImage />
      </div>
    </AppShell>
  );
};
