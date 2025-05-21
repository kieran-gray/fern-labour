import { motion } from 'motion/react';
import { Container, Image, Text, Title } from '@mantine/core';
import classes from './Story.module.css';

export type StoryProps = {
  title?: string;
  body?: string;
  imageSrc?: string;
  imageAlt?: string;
};

export function Story01({ title, body, imageSrc, imageAlt }: StoryProps) {
  return (
    <motion.div
      initial={{ opacity: 0.0, x: -200 }}
      whileInView={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.8, delay: 0.2, ease: 'easeInOut' }}
      viewport={{ once: true }}
      style={{ height: '100%' }}
    >
      <Container size="lg" className={classes.container} id="#home">
        <div className={classes.inner}>
          <div className={classes.content}>
            <Title order={2} className={classes.title}>
              {title}
            </Title>
            <div className={classes.flexRow}>
              <Image src={imageSrc} className={classes.smallImage} alt={imageAlt} />
            </div>
            <Text mt="md" className={classes.text}>
              {body}
            </Text>
          </div>
          <Image
            src={imageSrc}
            className={classes.bigImage}
            style={{ padding: '20px' }}
            alt={imageAlt}
          />
        </div>
      </Container>
    </motion.div>
  );
}
