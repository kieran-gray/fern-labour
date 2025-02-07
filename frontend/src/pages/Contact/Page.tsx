import { FooterSimple } from '../../shared-components/Footer/Footer';
import { Header } from '../../shared-components/Header/Header';
import { ContactUs } from './ContactUs/ContactUs';

export const ContactPage = () => {
  return (
    <div style={{ height: '100svh', display: 'flex', flexDirection: 'column' }}>
      <Header active="" />
      <div style={{ padding: '15px' }}>
        <ContactUs />
      </div>
      <div style={{ flexGrow: 1 }} />
      <FooterSimple />
    </div>
  );
};
