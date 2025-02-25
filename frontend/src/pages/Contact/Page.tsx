import { AppShell } from '../../shared-components/AppShell';
import { ContactUs } from './ContactUs/ContactUs';
import baseClasses from '../../shared-components/shared-styles.module.css';

export const ContactPage = () => {
  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <ContactUs />
      </div>
    </AppShell>
  );
};
