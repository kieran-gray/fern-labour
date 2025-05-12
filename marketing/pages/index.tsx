import { ContactMessageFloating } from '@/components/ContactMessageFloating/ContactMessageFloating';
import { FooterSimple } from '@/components/Footer/Footer';
import { LandingPage } from '@/components/Landing/Page';
import { Header01 } from '@/components/PillHeader/PillHeader';

export default function HomePage() {
  return (
    <>
      <Header01
        breakpoint="sm"
        callToActionTitle="Go to app"
        callToActionUrl={process.env.NEXT_PUBLIC_FRONTEND_URL}
        h="80"
        radius="50px"
      />
      <LandingPage callToActionUrl={process.env.NEXT_PUBLIC_FRONTEND_URL} />
      <ContactMessageFloating />
      <FooterSimple />
    </>
  );
}
