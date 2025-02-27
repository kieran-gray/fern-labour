import { motion } from 'motion/react';
import { Container, Image, Text, Title } from '@mantine/core';
import classes from './Story.module.css';

export function Story03() {
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
              Loved ones are automatically notified when labour begins
            </Title>
            <div className={classes.flexRow}>
              <Image
                src="images/AutomaticUpdates.svg"
                className={classes.smallImage}
                alt="people talking"
              />
            </div>
            <Text mt="md" className={classes.text}>
              When you start tracking contractions, we’ll instantly notify your subscribers in their
              preferred way.
              <br />
              <br />
              Track your labour and share live updates on your terms, all in one place.
            </Text>
          </div>
          <Image
            src="images/AutomaticUpdates.svg"
            className={classes.bigImage}
            alt="people talking"
          />
        </div>
      </Container>
    </motion.div>
  );
}
