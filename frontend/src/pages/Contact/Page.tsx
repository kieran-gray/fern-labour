import { ContactUs } from './ContactUs/ContactUs';
import baseClasses from '../../shared-components/shared-styles.module.css';
import { AppShell } from '../../shared-components/AppShell';

export const ContactPage = () => {
  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <ContactUs />
      </div>
    </AppShell>
  );
};
