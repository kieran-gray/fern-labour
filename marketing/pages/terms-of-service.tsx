import Head from 'next/head';
import { FooterSimple } from '@/components/Footer/Footer';
import { Header01 } from '@/components/PillHeader/PillHeader';
import { TermsOfServicePageContent } from '@/components/TermsOfService/Page';

export default function TermsOfServicePage() {
  return (
    <>
      <Head>
        <meta property="og:title" content="Understand Your Rights: Fern Labour Terms of Service" />
        <meta
          property="og:description"
          content="Learn about your data rights and privacy with Fern Labour."
        />
        <meta property="og:url" content="https://fernlabour.com/terms-of-service" />
      </Head>
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
