import { Space } from '@mantine/core';
import { CallToAction01 } from './CallToAction/CallToAction';
import { FaqWithImage } from './FAQ/FaqWithImage';
import { FeaturesDemo } from './FeaturesCarousel/FeaturesCarousel';
import { Feature02 } from './FeaturesMotion/FeaturesMotion';
import { Hero03 } from './HeroMotion/HeroMotion';
import {
  CallToActionText,
  HeroText,
  PricingText,
  Story01Text,
  Story02Text,
  Story03Text,
  Story04Text,
} from './LandingPageCopy';
import { Pricing01 } from './Pricing/Pricing';
import { Story01 } from './StoryTelling/Story-01';
import { Story02 } from './StoryTelling/Story-02';
import { Story03 } from './StoryTelling/Story-03';
import { Story04 } from './StoryTelling/Story-04';

type LandingPageProps = {
  /** URL for the call to action button */
  callToActionUrl?: string;
};

export const LandingPage = ({ callToActionUrl = '#' }: LandingPageProps) => {
  return (
    <div style={{ padding: '15px' }}>
      <Hero03 {...HeroText} />
      <div style={{ overflow: 'hidden' }}>
        <Story01 {...Story01Text} />
        <Space h="xl" />
        <Story02 {...Story02Text} />
        <Space h="xl" />
        <Story03 {...Story03Text} />
        <Space h="xl" />
        <Story04 {...Story04Text} />
      </div>
      <Feature02 />
      <Pricing01 callToActionUrl={callToActionUrl} {...PricingText} />
      <FeaturesDemo />
      <FaqWithImage />
      <CallToAction01 {...CallToActionText} />
    </div>
  );
};
