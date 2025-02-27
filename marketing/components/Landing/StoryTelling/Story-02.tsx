import { motion } from 'motion/react';
import { Container, Image, Text, Title } from '@mantine/core';
import classes from './Story.module.css';

export function Story02() {
  return (
    <motion.div
      initial={{ opacity: 0.0, x: 200 }}
      whileInView={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.8, delay: 0.2, ease: 'easeInOut' }}
      viewport={{ once: true }}
      style={{ height: '100%' }}
    >
      <Container size="lg" className={classes.container} id="#home">
        <div className={classes.inner}>
          <Image src="images/Meditate.svg" className={classes.bigImage} alt="woman meditating" />
          <div className={classes.content}>
            <Title order={2} className={classes.title}>
              Effortless updates during your labour journey
            </Title>
            <div className={classes.flexRow}>
              <Image
                src="images/Meditate.svg"
                className={classes.smallImage}
                alt="woman meditating"
              />
            </div>
            <Text mt="md" className={classes.text}>
              With our app, you don’t have to keep answering.
              <br />
              <br />
              Friends and family can check for updates themselves, so you can focus on resting,
              preparing, and getting through labour your way.
            </Text>
          </div>
        </div>
      </Container>
    </motion.div>
  );
}
