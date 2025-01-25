import { FooterSimple } from '@/components/Footer/Footer';
import { Header } from '@/components/Header/Header';
import { NotFoundPage } from '@/components/NotFound/Page';

export default function Contact() {
  return (
    <div style={{ height: '100svh', display: 'flex', flexDirection: 'column' }}>
      <Header page="contact" />
      <NotFoundPage />
      <FooterSimple />
    </div>
  );
}
