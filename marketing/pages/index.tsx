import { FooterSimple } from '@/components/Footer/Footer';
import { LandingPage } from '@/components/Landing/Page';
import { Header01 } from '@/components/PillHeader/PillHeader';

export default function HomePage() {
  return (
    <>
      <Header01
        breakpoint="sm"
        callToActionTitle="Go to app"
        callToActionUrl="http://localhost:5173"
        h="80"
        radius="50px"
      />
      <LandingPage />
      <FooterSimple />
    </>
  );
}
