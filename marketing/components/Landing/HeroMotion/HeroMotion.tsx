import Link from 'next/link';
import { IconArrowRight } from '@tabler/icons-react';
import { motion } from 'motion/react';
import { Box, Button, Container, ContainerProps, Flex, Stack, Text } from '@mantine/core';
import { JumboTitle } from '../JumboTitle/JumboTitle';
import classes from './HeroMotion.module.css';

type Hero03Props = ContainerProps & {
  title?: string;
  description?: string;
};

export const Hero03 = ({ title, description, ...containerProps }: Hero03Props) => (
  <Container
    pos="relative"
    h="80vh"
    mah={600}
    style={{ overflow: 'hidden' }}
    px="15px"
    fluid
    id="#home"
  >
    <Container component="section" h="80vh" mah={600} mx="auto" size="xl" {...containerProps}>
      <Box
        pos="absolute"
        top={0}
        left={0}
        h="100%"
        w="100%"
        className={classes['vertical-backdrop']}
      />
      <Flex h="100%" align="center" pos="relative" justify="center">
        <Stack
          pt={{ base: 'xl', sm: 0 }}
          maw="var(--mantine-breakpoint-md)"
          align="center"
          gap="lg"
          style={{ zIndex: 1 }}
        >
          <motion.div
            initial={{ opacity: 0.0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: 'easeInOut' }}
            viewport={{ once: true }}
          >
            <JumboTitle ta="center" order={1} fz="lg" style={{ textWrap: 'balance' }}>
              {title}
            </JumboTitle>
          </motion.div>
          <motion.div
            initial={{ opacity: 0.0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4, ease: 'easeInOut' }}
            viewport={{ once: true }}
          >
            <Text
              ta="center"
              maw="var(--mantine-breakpoint-xs)"
              fz="xl"
              style={{ textWrap: 'balance' }}
            >
              {description}
            </Text>
          </motion.div>
          <motion.div
            initial={{ opacity: 0.0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.6, ease: 'easeInOut' }}
            viewport={{ once: true }}
          >
            <Link href="https://track.fernlabour.com" target="_blank">
              <Button
                radius="xl"
                size="lg"
                className={classes.control}
                rightSection={<IconArrowRight />}
              >
                Start tracking free
              </Button>
            </Link>
          </motion.div>
        </Stack>
      </Flex>
    </Container>
  </Container>
);
