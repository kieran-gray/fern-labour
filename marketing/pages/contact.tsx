import { ContactPage } from '@/components/Contact/Page';
import { FooterSimple } from '@/components/Footer/Footer';
import { Header01 } from '@/components/PillHeader/PillHeader';

export default function Contact() {
  return (
    <div style={{ height: '100svh', display: 'flex', flexDirection: 'column' }}>
      <Header01
        breakpoint="sm"
        callToActionTitle="Go to app"
        callToActionUrl={process.env.NEXT_PUBLIC_FRONTEND_URL}
        h="80"
        radius="50px"
        landingPage={false}
      />
      <ContactPage />
      <FooterSimple />
    </div>
  );
}
