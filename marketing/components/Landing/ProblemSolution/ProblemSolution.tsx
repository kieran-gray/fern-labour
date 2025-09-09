// Using a standard <img> with srcSet for responsive images
import { motion } from 'motion/react';
import { Box, Container, Stack, Text, Title } from '@mantine/core';
import { JumboTitle } from '../JumboTitle/JumboTitle';
import classes from './ProblemSolution.module.css';

type Feature = {
  title: string;
  description: string;
  screenshotAlt: string;
  imageBaseName: string;
};

type FeaturesProps = {
  features: Feature[];
};

export const ProblemSolution = ({ features }: FeaturesProps) => {
  return (
    <Box py={80}>
      <Container size="xl">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          viewport={{ once: true }}
        >
          <JumboTitle order={2} fz="xs" ta="center" style={{ textWrap: 'balance' }} mb={80}>
            Keep Family Close. Keep Stress Away.
          </JumboTitle>
        </motion.div>

        <Stack gap={60}>
          {features.map((feature, index) => {
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, ease: 'easeOut', delay: index * 0.1 }}
                viewport={{ once: true, margin: '-100px' }}
              >
                <Container size="lg" className={classes.container}>
                  <div className={classes.inner}>
                    <Box className={classes.phoneContainer}>
                      <img
                        src={`/images/features/563x1218/${feature.imageBaseName}.webp`}
                        srcSet={`
                          /images/features/281x609/${feature.imageBaseName}.webp 281w,
                          /images/features/563x1218/${feature.imageBaseName}.webp 563w,
                          /images/features/1125x2436/${feature.imageBaseName}.webp 1125w
                        `}
                        sizes="(max-width: 480px) 160px, (max-width: 768px) 200px, (max-width: 1200px) 240px, 280px"
                        alt={feature.screenshotAlt}
                        className={classes.phoneImage}
                        loading={index < 2 ? 'eager' : 'lazy'}
                        decoding="async"
                        width={563}
                        height={1218}
                      />
                    </Box>

                    {/* Content */}
                    <div className={classes.content}>
                      <Title order={3} className={classes.title}>
                        {feature.title}
                      </Title>

                      <Text
                        size="lg"
                        c="var(--mantine-color-gray-7)"
                        className={classes.description}
                        style={{ lineHeight: 1.6 }}
                      >
                        {feature.description}
                      </Text>
                    </div>
                  </div>
                </Container>
              </motion.div>
            );
          })}
        </Stack>
      </Container>
    </Box>
  );
};
