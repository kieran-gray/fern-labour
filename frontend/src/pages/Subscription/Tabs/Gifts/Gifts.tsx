import { ImportantText } from '@shared/ImportantText/ImportantText';
import { PageContainerContentBottom } from '@shared/PageContainer/PageContainer';
import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { pluraliseName } from '@shared/utils';
import { Badge, Box, Button, Flex, Image, Text } from '@mantine/core';
import dbhf_main from './ads/dbhf/main.jpg';
import my1styears_desktop from './ads/my1styears/desktop.jpg';
import my1styears_main from './ads/my1styears/main.webp';
import etta_loves_main from './ads/etta-loves/img6-1699887317359.png'
import thortful_main from './ads/thortful/Thortful_cover_photo.webp'
import pure_earth_collection_main from './ads/pureearthcollection/main.jpg';
import zello_main from './ads/zello/main.jpg';
import image from './Gifts.svg';
import baseClasses from '@shared/shared-styles.module.css';

export default function Gifts({ birthingPersonName }: { birthingPersonName: string }) {
  const pluralisedBirthingPersonName = pluraliseName(birthingPersonName);

  const gifts = [
    {
      title: 'My 1st Years',
      subtitle: 'Personalised Baby Gifts to Treasure Forever',
      text: `Celebrate ${pluralisedBirthingPersonName} new arrival with a heartfelt, personalised baby gift.
  From classic teddy bears and snuggly blankets to tiny trainers and keepsakes, each item is designed to become part of the family story, cherished from their first days and beyond.`,
      note: '👉 Give a gift that says: “Welcome to the world.”',
      mobileImage: (
        <Image
          hiddenFrom="md"
          src={my1styears_main}
          alt="My 1st Years"
          style={{ maxHeight: '250px', width: '100%', margin: 'auto' }}
        />
      ),
      desktopImage: (
        <Image
          visibleFrom="md"
          src={my1styears_desktop}
          alt="My 1st Years"
          style={{ maxWidth: '250px', width: '100%' }}
        />
      ),
      url: 'https://tidd.ly/3EL2r6X',
      cta: 'Shop My 1st Years',
      featured: true,
    },
    {
      title: 'Etta Loves',
      subtitle: 'Science-Backed Baby Essentials for Visual Development',
      text: `Support ${birthingPersonName} with beautifully designed muslins, playmats and comforters that do more than look good. 
  Etta Loves’ patterns are developed with an expert in infant vision, carefully crafted to stimulate little eyes and support cognitive development from day one. It’s a gift that combines practicality, comfort, and science-led care.`,
      note: '👉 A thoughtful way to say: “Growing minds deserve beauty and science.”',
      mobileImage: (
        <Image
          hiddenFrom="md"
          src={etta_loves_main}
          alt="Etta Loves"
          style={{ maxHeight: '250px', maxWidth: '320px', width: '100%', margin: 'auto' }}
          loading="lazy"
        />
      ),
      desktopImage: (
        <Image
          visibleFrom="md"
          src={etta_loves_main}
          alt="Etta Loves"
          style={{ maxHeight: '400px', maxWidth: '450px', width: '100%' }}
          loading="lazy"
        />
      ),
      url: 'https://tidd.ly/4pfGfUR',
      cta: 'Explore Etta Loves',
    },
    {
      title: 'Don’t Buy Her Flowers',
      subtitle: 'Thoughtful Hampers for New Mums',
      text: `Because what most new mums really need isn’t flowers, it’s rest, care, and a little extra support.
  
  These beautifully curated gift boxes are packed with practical treats and calming comforts, from snacks and teas to cosy loungewear and skincare. Whether it’s for your partner, daughter, friend or colleague, this is the kind of TLC that truly helps.`,
      note: '👉 A perfect way to say: “You’ve got this, and I’ve got you.”',
      mobileImage: (
        <Image
          hiddenFrom="md"
          src={dbhf_main}
          alt="Don’t Buy Her Flowers"
          style={{ maxHeight: '250px', maxWidth: '320px', width: '100%', margin: 'auto' }}
          loading="lazy"
        />
      ),
      desktopImage: (
        <Image
          visibleFrom="md"
          src={dbhf_main}
          alt="Don’t Buy Her Flowers"
          style={{ maxHeight: '400px', maxWidth: '450px', width: '100%' }}
          loading="lazy"
        />
      ),
      url: 'https://tidd.ly/3FHKzKi',
      cta: 'Build a Gift Box',
    },
    {
      title: 'Zello Sleep',
      subtitle: 'White Noise Machines for Peaceful Nights',
      text: `Zello’s beautifully designed white noise machines help babies fall asleep faster and stay asleep longer by mimicking the soothing sounds of the womb. Trusted by thousands of parents, they create a calm, consistent sleep environment that supports healthy bedtime routines for baby and the whole household.`,
      note: '👉 A perfect way to say: “Rest easy, little one.”',
      mobileImage: (
        <Image
          hiddenFrom="md"
          src={zello_main}
          alt="Zello Sleep"
          style={{ maxHeight: '250px', maxWidth: '320px', width: '100%', margin: 'auto' }}
          loading="lazy"
        />
      ),
      desktopImage: (
        <Image
          visibleFrom="md"
          src={zello_main}
          alt="Zello Sleep"
          style={{ maxHeight: '400px', maxWidth: '450px', width: '100%' }}
          loading="lazy"
        />
      ),
      url: 'https://tidd.ly/4kCWecK',
      cta: 'Shop Zello Sleep',
    },
    {
      title: 'Pure Earth Collection',
      subtitle: 'Natural, Non-Toxic Products for Growing Families',
      text: `From baby sleepwear to eco-friendly lunchboxes, Pure Earth Collection offers beautifully designed products made with your child’s health and the planet in mind.
  Created by parents, for parents, their award-winning range uses only natural, biodegradable materials, completely free from harmful chemicals. It’s a thoughtful choice for anyone wanting safer, more sustainable essentials as little ones grow.`,
      note: '👉 A meaningful way to say: “Healthy kids, healthy planet.”',
      mobileImage: (
        <Image
          hiddenFrom="md"
          src={pure_earth_collection_main}
          alt="Pure Earth Collection"
          style={{ maxHeight: '250px', maxWidth: '320px', width: '100%', margin: 'auto' }}
          loading="lazy"
        />
      ),
      desktopImage: (
        <Image
          visibleFrom="md"
          src={pure_earth_collection_main}
          alt="Pure Earth Collection"
          style={{ maxHeight: '400px', maxWidth: '450px', width: '100%' }}
          loading="lazy"
        />
      ),
      url: 'https://tidd.ly/436fwA0',
      cta: 'Shop Pure Earth',
    },
    {
      title: 'Thortful',
      subtitle: 'Unique Cards & Thoughtful Touches for Every Occasion',
      text: `Sometimes, the simplest gesture means the most. Thortful offers a huge collection of beautifully designed cards from independent creators, perfect for celebrating ${pluralisedBirthingPersonName} new journey into parenthood. 
  Add a handwritten message, or include a little extra gift like chocolates or flowers, to make it even more personal.`,
      note: '👉 A heartfelt way to say: “I’m thinking of you.”',
      mobileImage: (
        <Image
          hiddenFrom="md"
          src={thortful_main}
          alt="Thortful"
          style={{ maxHeight: '250px', maxWidth: '320px', width: '100%', margin: 'auto' }}
          loading="lazy"
        />
      ),
      desktopImage: (
        <Image
          visibleFrom="md"
          src={thortful_main}
          alt="Thortful"
          style={{ maxHeight: '400px', maxWidth: '450px', width: '100%' }}
          loading="lazy"
        />
      ),
      url: 'https://thortful.pxf.io/GKJXqV',
      cta: 'Browse Thortful Cards',
    },
  ];

  const description = `Help support ${birthingPersonName} with meaningful, practical gifts for the early days of parenthood. From nourishing meals to personal keepsakes, here are a few special ways to show your love, without asking “Do you need anything?”`;

  return (
    <>
      <PageContainerContentBottom
        title="Thoughtful Gifts for New Parents"
        description={description}
        image={image}
        mobileImage={image}
      >
        <ImportantText message="Some of our links are affiliate links, which help support the app at no extra cost to you." />
      </PageContainerContentBottom>
      {gifts.map((gift, index) => (
        <div key={gift.title} className={baseClasses.root} style={{ marginTop: '20px' }}>
          <div className={baseClasses.body}>
            <div className={baseClasses.inner}>
              <div className={baseClasses.content}>
                <div className={baseClasses.flexRowNoBP}>
                  <ResponsiveTitle title={gift.title} />
                {gift.featured && (
                  <div style={{ display: 'flex', justifyContent: 'center', marginTop: 8 }}>
                    <Badge color="pink" variant="light">Featured</Badge>
                  </div>
                )}
                </div>
                <ResponsiveDescription description={gift.subtitle} marginTop={6} />
                <Flex
                  direction={{ base: 'column', md: index % 2 === 0 ? 'row' : 'row-reverse' }}
                  gap="xl"
                  align="center"
                  mt="md"
                >
                  <Box style={{ flexGrow: 1, width: '100%' }}>
                    <a
                      href={gift.url}
                      target="_blank"
                      rel="sponsored noopener noreferrer"
                      aria-label={`Visit ${gift.title}`}
                      style={{ display: 'block' }}
                    >
                    {gift.desktopImage}
                    </a>
                  </Box>
                  <Box>
                    {gift.mobileImage}
                    <Text mb="sm" mt="md" size="sm" hiddenFrom="sm">
                      {gift.text}
                    </Text>
                    <Text mb="sm" mt="md" size="md" visibleFrom="sm">
                      {gift.text}
                    </Text>
                    <Text fs="italic" mb="xl" size="sm" hiddenFrom="sm">
                      {gift.note}
                    </Text>
                    <Text fs="italic" mb="xl" size="md" visibleFrom="sm">
                      {gift.note}
                    </Text>
                    <div
                      style={{
                        display: 'flex',
                        flexDirection: 'row',
                        width: '100%',
                        justifyContent: 'center',
                      }}
                    >
                      <Button
                        component="a"
                        href={gift.url}
                        target="_blank"
                        visibleFrom="md"
                        rel="sponsored noopener noreferrer"
                        variant="light"
                        size="md"
                        radius="xl"
                        style={{ width: '50%' }}
                        aria-label={`Visit ${gift.title}`}
                      >
                        {gift.cta ?? 'View Gift'}
                      </Button>
                      <Button
                        component="a"
                        href={gift.url}
                        target="_blank"
                        hiddenFrom="md"
                        rel="sponsored noopener noreferrer"
                        variant="filled"
                        size="md"
                        radius="xl"
                        style={{ width: '100%' }}
                        aria-label={`Visit ${gift.title}`}
                      >
                        {gift.cta ?? 'View Gift'}
                      </Button>
                    </div>
                  </Box>
                </Flex>
              </div>
            </div>
          </div>
        </div>
      ))}
    </>
  );
}
