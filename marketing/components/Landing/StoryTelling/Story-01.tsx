import { motion } from 'motion/react';
import { Container, Image, Text, Title } from '@mantine/core';
import classes from './Story.module.css';

export function Story01() {
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
              Only 4% of women give birth on their due date
            </Title>
            <div className={classes.flexRow}>
              <Image
                src="images/ComingSoon.svg"
                className={classes.smallImage}
                alt="clock and calendar"
              />
            </div>
            <Text mt="md" className={classes.text}>
              That means a lot of waiting, guessing, and unfortunately, constant messages asking:
              "Any news?"
            </Text>
          </div>
          <Image
            src="images/ComingSoon.svg"
            className={classes.comingSoonImageBig}
            style={{ padding: '20px' }}
            alt="clock and calendar"
          />
        </div>
      </Container>
    </motion.div>
  );
}
