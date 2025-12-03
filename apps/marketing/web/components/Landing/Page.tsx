import { Space } from '@mantine/core';
import { FaqWithImage } from './FAQ/FaqWithImage';
import { Feature02 } from './FeaturesMotion/FeaturesMotion';
import { FinalCTA } from './FinalCTA/FinalCTA';
import { Hero03 } from './HeroMotion/HeroMotion';
import {
  CallToActionText,
  HeroText,
  PricingText,
  ProblemSolutionText,
  SocialProofTrustText,
} from './LandingPageCopy';
import { Pricing01 } from './Pricing/Pricing';
import { ProblemSolution } from './ProblemSolution/ProblemSolution';
import { SocialProofTrust } from './SocialProofTrust/SocialProofTrust';

type LandingPageProps = {
  /** URL for the call to action button */
  callToActionUrl?: string;
};

export const LandingPage = ({ callToActionUrl = '#' }: LandingPageProps) => {
  return (
    <>
      <Hero03 {...HeroText} />
      <ProblemSolution {...ProblemSolutionText} />
      <Space h={40} />
      <Feature02 title="How Fern Labour Works" />
      <SocialProofTrust {...SocialProofTrustText} />
      <Pricing01 callToActionUrl={callToActionUrl} {...PricingText} />
      <FaqWithImage />
      <FinalCTA {...CallToActionText} />
    </>
  );
};
