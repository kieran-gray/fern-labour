import { Header } from '@/components/Header/Header';
import { FooterSimple } from '@/components/Footer/Footer';
import { LandingPage } from '@/components/Landing/Page';

export default function HomePage() {
  return (
    <>
      <Header page='home' />
      <LandingPage />
      <FooterSimple />
    </>
  );
}
