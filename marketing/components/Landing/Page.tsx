import { Container, Space } from '@mantine/core';
import { CallToAction01 } from './CallToAction/CallToAction';
import { FaqWithImage } from './FAQ/FaqWithImage';
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
    <>
      <Hero03 {...HeroText} />
      <Container
        bg="var(--mantine-color-body)"
        py="calc(var(--mantine-spacing-lg) * 3)"
        px="15px"
        fluid
        style={{ overflow: 'hidden' }}
      >
        <Story01 {...Story01Text} />
        <Space h="md" />
        <Story02 {...Story02Text} />
        <Space h="md" />
        <Story03 {...Story03Text} />
        <Space h="md" />
        <Story04 {...Story04Text} />
      </Container>
      <Feature02 />
      <Pricing01 callToActionUrl={callToActionUrl} {...PricingText} />
      <FaqWithImage />
      <CallToAction01 {...CallToActionText} />
    </>
  );
};
