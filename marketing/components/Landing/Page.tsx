import { Space } from '@mantine/core';
import { FaqWithImage } from './FAQ/FaqWithImage';
import { Feature02 } from './FeaturesMotion/FeaturesMotion';
import { Hero03 } from './HeroMotion/HeroMotion';
import { Pricing01 } from './Pricing/Pricing';
import { Story01 } from './StoryTelling/Story-01';
import { Story02 } from './StoryTelling/Story-02';
import { Story03 } from './StoryTelling/Story-03';

type LandingPageProps = {
  /** URL for the call to action button */
  callToActionUrl?: string;
};

export const LandingPage = ({ callToActionUrl = '#' }: LandingPageProps) => {
  return (
    <div style={{ padding: '15px' }}>
      <Hero03 />
      <div style={{ overflow: 'hidden' }}>
        <Story01 />
        <Space h="xl" />
        <Story02 />
        <Space h="xl" />
        <Story03 />
      </div>
      <Feature02 />
      <Pricing01 callToActionUrl={callToActionUrl} />
      <FaqWithImage />
    </div>
  );
};
