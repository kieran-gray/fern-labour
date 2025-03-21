'use client';

import { Container, Image } from '@mantine/core';
import { JumboTitle } from '../JumboTitle/JumboTitle';
import { Carousel } from '@mantine/carousel';
import classes from './FeaturesCarousel.module.css';

export function FeaturesCarousel() {
  return (
    <Carousel
      withIndicators
      height="100%"
      slideSize={{ base: "33.33333%" }}
      slideGap="xs"
      type='container'
      loop
      align="start"
      pos='relative'
    >
      <Carousel.Slide><Image src="images/features/01.png" className={classes.image} /></Carousel.Slide>
      <Carousel.Slide><Image src="images/features/02.png" className={classes.image} /></Carousel.Slide>
      <Carousel.Slide><Image src="images/features/03.png" className={classes.image} /></Carousel.Slide>
      <Carousel.Slide><Image src="images/features/04.png" className={classes.image} /></Carousel.Slide>
      <Carousel.Slide><Image src="images/features/05.png" className={classes.image} /></Carousel.Slide>
      <Carousel.Slide><Image src="images/features/06.png" className={classes.image} /></Carousel.Slide>
      <Carousel.Slide><Image src="images/features/07.png" className={classes.image} /></Carousel.Slide>
    </Carousel>
  );
}

export const FeaturesDemo= () => (
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
