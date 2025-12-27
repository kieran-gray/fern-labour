export interface GiftAdData {
  id: string;
  title: string;
  subtitle: string;
  text: (birthingPersonName: string) => string;
  note: string;
  url: string;
  cta: string;
  featured?: boolean;
  mobileImagePath: string;
  desktopImagePath: string;
}

export const giftAds: GiftAdData[] = [
  {
    id: 'my1styears',
    title: 'My 1st Years',
    subtitle: 'Personalised Baby Gifts to Treasure Forever',
    text: (birthingPersonName: string) =>
      `Celebrate ${birthingPersonName.endsWith('s') ? `${birthingPersonName}'` : `${birthingPersonName}'s`} new arrival with a heartfelt, personalised baby gift.
  From classic teddy bears and snuggly blankets to tiny trainers and keepsakes, each item is designed to become part of the family story, cherished from their first days and beyond.`,
    note: '👉 Give a gift that says: "Welcome to the world."',
    url: 'https://tidd.ly/3EL2r6X',
    cta: 'Shop My 1st Years',
    featured: true,
    mobileImagePath: 'my1styears/main.webp',
    desktopImagePath: 'my1styears/desktop.jpg',
  },
  {
    id: 'etta-loves',
    title: 'Etta Loves',
    subtitle: 'Science-Backed Baby Essentials for Visual Development',
    text: (birthingPersonName: string) =>
      `Support ${birthingPersonName} with beautifully designed muslins, playmats and comforters that do more than look good.
  Etta Loves' patterns are developed with an expert in infant vision, carefully crafted to stimulate little eyes and support cognitive development from day one. It's a gift that combines practicality, comfort, and science-led care.`,
    note: '👉 A thoughtful way to say: "Growing minds deserve beauty and science."',
    url: 'https://tidd.ly/4pfGfUR',
    cta: 'Explore Etta Loves',
    mobileImagePath: 'etta-loves/img6-1699887317359.png',
    desktopImagePath: 'etta-loves/img6-1699887317359.png',
  },
  {
    id: 'dbhf',
    title: 'Don`t Buy Her Flowers',
    subtitle: 'Thoughtful Hampers for New Mums',
    text: () =>
      `Because what most new mums really need isn't flowers, it's rest, care, and a little extra support.

  These beautifully curated gift boxes are packed with practical treats and calming comforts, from snacks and teas to cosy loungewear and skincare. Whether it's for your partner, daughter, friend or colleague, this is the kind of TLC that truly helps.`,
    note: '👉 A perfect way to say: "You`ve got this, and I`ve got you."',
    url: 'https://tidd.ly/3FHKzKi',
    cta: 'Build a Gift Box',
    mobileImagePath: 'dbhf/main.jpg',
    desktopImagePath: 'dbhf/main.jpg',
  },
  {
    id: 'zello',
    title: 'Zello Sleep',
    subtitle: 'White Noise Machines for Peaceful Nights',
    text: () =>
      `Zello's beautifully designed white noise machines help babies fall asleep faster and stay asleep longer by mimicking the soothing sounds of the womb. Trusted by thousands of parents, they create a calm, consistent sleep environment that supports healthy bedtime routines for baby and the whole household.`,
    note: '👉 A perfect way to say: "Rest easy, little one."',
    url: 'https://tidd.ly/4kCWecK',
    cta: 'Shop Zello Sleep',
    mobileImagePath: 'zello/main.jpg',
    desktopImagePath: 'zello/main.jpg',
  },
  {
    id: 'pure-earth-collection',
    title: 'Pure Earth Collection',
    subtitle: 'Natural, Non-Toxic Products for Growing Families',
    text: () =>
      `From baby sleepwear to eco-friendly lunchboxes, Pure Earth Collection offers beautifully designed products made with your child's health and the planet in mind.
  Created by parents, for parents, their award-winning range uses only natural, biodegradable materials, completely free from harmful chemicals. It's a thoughtful choice for anyone wanting safer, more sustainable essentials as little ones grow.`,
    note: '👉 A meaningful way to say: "Healthy kids, healthy planet."',
    url: 'https://tidd.ly/436fwA0',
    cta: 'Shop Pure Earth',
    mobileImagePath: 'pureearthcollection/main.jpg',
    desktopImagePath: 'pureearthcollection/main.jpg',
  },
  {
    id: 'thortful',
    title: 'Thortful',
    subtitle: 'Unique Cards & Thoughtful Touches for Every Occasion',
    text: (birthingPersonName: string) =>
      `Sometimes, the simplest gesture means the most. Thortful offers a huge collection of beautifully designed cards from independent creators, perfect for celebrating ${birthingPersonName.endsWith('s') ? `${birthingPersonName}'` : `${birthingPersonName}'s`} new journey into parenthood.
  Add a handwritten message, or include a little extra gift like chocolates or flowers, to make it even more personal.`,
    note: '👉 A heartfelt way to say: "I`m thinking of you."',
    url: 'https://thortful.pxf.io/GKJXqV',
    cta: 'Browse Thortful Cards',
    mobileImagePath: 'thortful/Thortful_cover_photo.webp',
    desktopImagePath: 'thortful/Thortful_cover_photo.webp',
  },
];
