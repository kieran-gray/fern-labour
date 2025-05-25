import { AppShell } from '@shared/AppShell';
import { ContactUs } from './ContactUs/ContactUs';
import baseClasses from '@shared/shared-styles.module.css';

export const ContactPage = () => {
  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <ContactUs />
      </div>
    </AppShell>
  );
};
