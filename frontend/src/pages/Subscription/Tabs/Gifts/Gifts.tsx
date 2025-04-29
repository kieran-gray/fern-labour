import { Box, Button, Flex, Image, Text } from '@mantine/core';
import { ResponsiveTitle } from '../../../../shared-components/ResponsiveTitle/ResponsiveTitle';
import { pluraliseName } from '../../../../shared-components/utils';
import dbhf_main from './ads/dbhf/main.jpg';
import my1styears_desktop from './ads/my1styears/desktop.jpg';
import my1styears_main from './ads/my1styears/main.webp';
import powfood_main from './ads/powfood/main.jpg';
import wildly_tasty_main from './ads/wildlytasty/main.webp';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from '../../../Labour/Tabs/Updates/LabourUpdates.module.css';

export default function Gifts({ birthingPersonName }: { birthingPersonName: string }) {
  const pluralisedBirthingPersonName = pluraliseName(birthingPersonName);

  const gifts = [
    {
      title: 'My 1st Years',
      subtitle: 'Personalised Baby Gifts to Treasure Forever',
      text: `Celebrate ${pluralisedBirthingPersonName} new arrival with a heartfelt, personalised baby gift.
  From classic teddy bears and snuggly blankets to tiny trainers and keepsakes, each item is designed to become part of the family story—cherished from their first days and beyond.`,
      note: '👉 Give a gift that says: “Welcome to the world.”',
      mobileImage: (
        <Image
          hiddenFrom="md"
          src={my1styears_main}
          alt="My 1st Years"
          style={{ maxHeight: '300px', width: '100%', margin: 'auto' }}
        />
      ),
      desktopImage: (
        <Image
          visibleFrom="md"
          src={my1styears_desktop}
          alt="My 1st Years"
          style={{ maxWidth: '300px', width: '100%' }}
        />
      ),
      url: 'https://tidd.ly/3EL2r6X',
    },
    {
      title: 'Don’t Buy Her Flowers',
      subtitle: 'Thoughtful Hampers for New Mums',
      text: `Because what most new mums really need isn’t flowers—it’s rest, care, and a little extra support.
  
  These beautifully curated gift boxes are packed with practical treats and calming comforts, from snacks and teas to cosy loungewear and skincare. Whether it’s for your partner, daughter, friend or colleague, this is the kind of TLC that truly helps.`,
      note: '👉 A perfect way to say: “You’ve got this—and I’ve got you.”',
      mobileImage: (
        <Image
          hiddenFrom="md"
          src={dbhf_main}
          alt="Don’t Buy Her Flowers"
          style={{ maxHeight: '250px', maxWidth: '400px', width: '100%', margin: 'auto' }}
        />
      ),
      desktopImage: (
        <Image
          visibleFrom="md"
          src={dbhf_main}
          alt="Don’t Buy Her Flowers"
          style={{ maxHeight: '400px', maxWidth: '450px', width: '100%' }}
        />
      ),
      url: 'https://tidd.ly/3FHKzKi',
    },
    {
      title: 'PowFood',
      subtitle: 'Nourishing Ready Meals for New Parents',
      text: `Make life easier for ${birthingPersonName} with a week of balanced, chef-prepared meals and snacks. 
  Frozen for freshness and designed for one-handed eating, these meals are faster and healthier than a takeaway—and ready in just 30 minutes. Includes a helpful guide to postpartum nutrition to support recovery and energy.`,
      note: '👉 A perfect way to say: “Take care of yourself.”',
      mobileImage: (
        <Image
          hiddenFrom="md"
          src={powfood_main}
          alt="PowFood"
          style={{ maxHeight: '250px', maxWidth: '400px', width: '100%', margin: 'auto' }}
        />
      ),
      desktopImage: (
        <Image
          visibleFrom="md"
          src={powfood_main}
          alt="PowFood"
          style={{ maxHeight: '400px', maxWidth: '450px', width: '100%' }}
        />
      ),
      url: 'https://tidd.ly/4lPGCDU',
    },
    {
      title: 'Wildly Tasty',
      subtitle: 'Delicious Family Meals, Ready in Minutes',
      text: `Support the whole household with a bundle of family-friendly meals that take the pressure off cooking.
  Packed with goodness and ready in minutes, these frozen meals help make those first few days easier for ${birthingPersonName} and their loved ones.`,
      note: '👉 A great gift for keeping everyone fed and happy.',
      mobileImage: (
        <Image
          hiddenFrom="md"
          src={wildly_tasty_main}
          alt="Wildly Tasty"
          style={{ maxHeight: '250px', maxWidth: '400px', width: '100%', margin: 'auto' }}
        />
      ),
      desktopImage: (
        <Image
          visibleFrom="md"
          src={wildly_tasty_main}
          alt="Wildly Tasty"
          style={{ maxHeight: '400px', maxWidth: '450px', width: '100%' }}
        />
      ),
      url: 'https://tidd.ly/4jApK2H',
    },
  ];

  const description = `Help support ${birthingPersonName} with meaningful, practical gifts for the early days of parenthood. From nourishing meals to personal keepsakes, here are a few special ways to show your love—without asking “Do you need anything?”`;

  return (
    <>
      <div className={baseClasses.root}>
        <div className={baseClasses.body}>
          <div className={classes.inner}>
            <div className={classes.content}>
              <ResponsiveTitle title="Thoughtful Gifts for New Parents" />
              <Text c="var(--mantine-color-gray-7)" mt="sm" mb="md">
                {description}
              </Text>
            </div>
          </div>
        </div>
      </div>
      {gifts.map((gift, index) => (
        <div className={baseClasses.root} style={{ marginTop: '20px' }}>
          <div className={baseClasses.body}>
            <div className={classes.inner}>
              <div className={classes.content}>
                <ResponsiveTitle title={gift.title} />
                <Text c="var(--mantine-color-gray-8)" mt="sm" mb="md">
                  {gift.subtitle}
                </Text>
                <Flex
                  key={gift.title}
                  direction={{ base: 'column', md: index % 2 === 0 ? 'row' : 'row-reverse' }}
                  gap="xl"
                  align="center"
                  mt="xl"
                >
                  {gift.desktopImage}
                  <Box>
                    {gift.mobileImage}
                    <Text mb="sm" mt="md">
                      {gift.text}
                    </Text>
                    <Text fs="italic" mb="xl">
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
                        rel="noopener noreferrer"
                        variant="light"
                        size="md"
                        radius="xl"
                        style={{ width: '50%' }}
                      >
                        View Gift
                      </Button>
                      <Button
                        component="a"
                        href={gift.url}
                        target="_blank"
                        hiddenFrom="md"
                        rel="noopener noreferrer"
                        variant="light"
                        size="md"
                        radius="xl"
                        style={{ width: '100%' }}
                      >
                        View Gift
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
