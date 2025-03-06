import { FooterSimple } from '@/components/Footer/Footer';
import { Header01 } from '@/components/PillHeader/PillHeader';
import { TermsOfServicePageContent } from '@/components/TermsOfService/Page';

export default function TermsOfServicePage() {
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
      <TermsOfServicePageContent />
      <FooterSimple />
    </>
  );
}
