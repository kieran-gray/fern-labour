'use client';

import { motion } from 'motion/react';
import { Carousel } from '@mantine/carousel';
import { Container, Image } from '@mantine/core';
import { JumboTitle } from '../JumboTitle/JumboTitle';
import classes from './FeaturesCarousel.module.css';

const images = [
  'images/features/01.webp',
  'images/features/02.webp',
  'images/features/03.webp',
  'images/features/04.webp',
  'images/features/05.webp',
  'images/features/06.webp',
  'images/features/07.webp',
];

export function FeaturesCarousel() {
  return (
    <motion.div
      initial={{ opacity: 0.0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.1, ease: 'easeInOut' }}
      viewport={{ once: true }}
      style={{ height: '100%' }}
    >
      <Carousel
        withIndicators
        height="100%"
        slideSize={{ base: '33.33333%' }}
        slideGap="xs"
        type="container"
        loop
        align="start"
        pos="relative"
      >
        {images.map((src) => (
          <Carousel.Slide>
            <Image src={src} className={classes.image} />
          </Carousel.Slide>
        ))}
      </Carousel>
    </motion.div>
  );
}

export const FeaturesDemo = () => (
  <Container
    bg="var(--mantine-color-body)"
    py={{
      base: 'calc(var(--mantine-spacing-lg) * 4)',
      xs: 'calc(var(--mantine-spacing-lg) * 5)',
      lg: 'calc(var(--mantine-spacing-lg) * 6)',
    }}
    fluid
  >
    <Container size="lg" px={0} style={{ position: 'relative' }} id="#features">
      <JumboTitle order={2} fz="md" style={{ textWrap: 'balance' }}>
        How it works
      </JumboTitle>
    </Container>
    <Container size="lg" p={0} mt="xl">
      <FeaturesCarousel />
    </Container>
  </Container>
);
