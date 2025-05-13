import { Metadata } from 'next';
import Head from 'next/head';
import { FooterSimple } from '@/components/Footer/Footer';
import { Header01 } from '@/components/PillHeader/PillHeader';
import { PrivacyPageContent } from '@/components/Privacy/Page';

export const metadata: Metadata = {
  title: 'Your Privacy Matters: Fern Labour’s Data Protection Guide',
  description: 'Learn about your data rights and privacy with Fern Labour.',
  metadataBase: new URL('https://fernlabour.com/privacy'),
};

export default function PrivacyPage() {
  return (
    <>
      <Head>
        <meta
          property="og:title"
          content="Your Privacy Matters: Fern Labour’s Data Protection Guide"
        />
        <meta
          property="og:description"
          content="Learn about your data rights and privacy with Fern Labour."
        />
        <meta property="og:url" content="https://fernlabour.com/privacy" />
      </Head>
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
