'use client';

import { motion } from 'motion/react';
import { Carousel } from '@mantine/carousel';
import { Container, Image } from '@mantine/core';
import classes from './FeaturesCarousel.module.css';

const images = [
  { src: 'images/features/01.webp', alt: 'Fern Labour Tracker home screen' },
  { src: 'images/features/02.webp', alt: 'Fern Labour Tracker contraction tracker' },
  { src: 'images/features/03.webp', alt: 'Fern Labour Tracker status updates' },
  { src: 'images/features/04.webp', alt: 'Fern Labour Tracker statistics' },
  { src: 'images/features/05.webp', alt: 'Fern Labour Tracker invites' },
  { src: 'images/features/06.webp', alt: 'Fern Labour Tracker security' },
  { src: 'images/features/07.webp', alt: 'Fern Labour Tracker announcements' },
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
        previousControlProps={{ 'aria-label': 'Previous Feature' }}
        nextControlProps={{ 'aria-label': 'Next Feature' }}
      >
        {images.map((imageData) => (
          <Carousel.Slide key={imageData.alt} id={imageData.alt}>
            <Image src={imageData.src} className={classes.image} alt={imageData.alt} />
          </Carousel.Slide>
        ))}
      </Carousel>
    </motion.div>
  );
}

export const FeaturesDemo = () => (
  <Container py="calc(var(--mantine-spacing-lg) * 3)" px="15px" fluid>
    <Container size="lg" p={0}>
      <FeaturesCarousel />
    </Container>
  </Container>
);
