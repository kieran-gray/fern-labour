import { AppShell } from '../../shared-components/AppShell';
import { NotFoundImage } from './Components/Image/Image';
import baseClasses from '../../shared-components/shared-styles.module.css';

export const NotFoundPage: React.FC = () => {
  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <NotFoundImage />
      </div>
    </AppShell>
  );
};
