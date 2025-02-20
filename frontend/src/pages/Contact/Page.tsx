import { Center } from '@mantine/core';
import { FooterSimple } from '../../shared-components/Footer/Footer';
import { Header } from '../../shared-components/Header/Header';
import { ContactUs } from './ContactUs/ContactUs';
import baseClasses from '../../shared-components/shared-styles.module.css';

export const ContactPage = () => {
  return (
    <div style={{ height: '100svh', display: 'flex', flexDirection: 'column' }}>
      <Header />
      <Center flex="shrink" p={15}>
        <div className={baseClasses.flexColumn}>
          <ContactUs />
        </div>
      </Center>
      <div style={{ flexGrow: 1 }} />
      <FooterSimple />
    </div>
  );
};
