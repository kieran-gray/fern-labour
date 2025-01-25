import { ContactPage } from '@/components/Contact/Page';
import { FooterSimple } from '@/components/Footer/Footer';
import { Header } from '@/components/Header/Header';

export default function Contact() {
  return (
    <div style={{ height: '100svh', display: 'flex', flexDirection: 'column' }}>
      <Header page="contact" />
      <ContactPage />
      <FooterSimple />
    </div>
  );
}
