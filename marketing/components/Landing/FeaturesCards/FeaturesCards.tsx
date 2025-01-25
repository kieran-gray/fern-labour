import {
  Card,
  Container,
  SimpleGrid,
  Text,
  Title,
  Image
} from '@mantine/core';
import classes from './FeaturesCards.module.css';

const data = [
  {
    title: 'Track contractions',
    description:
      'Track each contraction’s timing and intensity to help monitor your labor progress. Our simple interface helps you focus on what matters most during this important time.',
    image: '/images/Track.webp',
  },
  {
    title: 'Share your journey',
    description:
      'Choose exactly who receives updates about your labor journey. Family and friends can stay informed while you focus on bringing your baby into the world.',
    image: '/images/Share.webp',
  },
  {
    title: 'Keep loved ones updated',
    description:
      'Keep your support network informed with quick updates throughout your labor. Share important moments and progress with those who matter most.',
    image: '/images/Announcements.webp',
  },
];

export function FeaturesCards() {
  const features = data.map((feature) => (
    <Card key={feature.title} shadow="md" radius="md" className={classes.card} padding="xl">
      <Image src={feature.image} className={classes.image} alt={feature.title}/>
      <div>
      <Text fz="lg" fw={500} className={classes.cardTitle} mt="md">
        {feature.title}
      </Text>
      <Text fz="sm" mt="sm">
        {feature.description}
      </Text>
      </div>
    </Card>
  ));

  return (
    <Container size="lg" py="xl" className={classes.container} mt={20} id="#features">
      <Title order={2} className={classes.title} ta="center" mt="sm">
        Effortless updates during your labor journey
      </Title>

      <Text className={classes.description} ta="center" mt="md">
        <strong>Only 4% of women give birth on their due date.</strong> Skip the constant updates, and skip the group chats.
        Loved ones will be notified automatically when your labour begins.
      </Text>

      <SimpleGrid cols={{ base: 1, md: 3 }} spacing="xl" mt={50}>
        {features}
      </SimpleGrid>
    </Container>
  );
}