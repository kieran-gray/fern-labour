import { FooterSimple } from '@/components/Footer/Footer';
import { Header01 } from '@/components/PillHeader/PillHeader';
import { PrivacyPageContent } from '@/components/Privacy/Page';

export default function PrivacyPage() {
  return (
    <>
      <Header01
        breakpoint="sm"
        callToActionTitle="Go to app"
        callToActionUrl={process.env.NEXT_PUBLIC_FRONTEND_URL}
        h="80"
        radius="50px"
        landingPage={false}
      />
      <PrivacyPageContent />
      <FooterSimple />
    </>
  );
}
