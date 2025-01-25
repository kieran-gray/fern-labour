import { FaqSimple } from './FaqSimple/FaqSimple';
import { FeaturesCards } from './FeaturesCards/FeaturesCards';
import { HeroBullets } from './HeroBullets/HeroBullets';

export const LandingPage = () => {
  return (
    <div style={{ padding: '15px' }}>
      <HeroBullets />
      <FeaturesCards />
      <FaqSimple />
    </div>
  );
};
