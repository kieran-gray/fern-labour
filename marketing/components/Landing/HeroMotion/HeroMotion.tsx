import Link from 'next/link';
import { IconArrowRight } from '@tabler/icons-react';
import { motion } from 'motion/react';
import { Badge, Box, Button, Container, ContainerProps, Flex, Stack, Text } from '@mantine/core';
import { JumboTitle } from '../JumboTitle/JumboTitle';
import classes from './HeroMotion.module.css';

type Hero03Props = ContainerProps & {
  badge?: string;
  title?: string;
  description?: string;
};

export const Hero03 = ({
  badge = 'For peace of mind at the end of your pregnancy',
  title = 'Share Your Birth Journey, On Your Terms',
  description = 'Real-time updates for family and friends, without the endless check-ins.',
  ...containerProps
}: Hero03Props) => (
  <Container pos="relative" h="100vh" mah={750} style={{ overflow: 'hidden' }} fluid>
    <Container component="section" h="100vh" mah={750} mx="auto" size="xl" {...containerProps}>
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
          {badge && (
            <motion.div
              initial={{ opacity: 0.0 }}
              transition={{ duration: 0.8, ease: 'easeInOut' }}
              viewport={{ once: true }}
              whileInView={{ opacity: 1 }}
            >
              <Badge
                variant="default"
                p="md"
                bg="var(--mantine-color-pink-5)"
                c="var(--mantine-color-white)"
                size="xl"
                mb="lg"
                style={{ textTransform: 'none', border: 'none' }}
                visibleFrom="sm"
              >
                {badge}
              </Badge>
              <Badge
                variant="default"
                p="md"
                bg="var(--mantine-color-pink-5)"
                c="var(--mantine-color-white)"
                size="lg"
                mb="lg"
                style={{ textTransform: 'none', border: 'none' }}
                hiddenFrom="sm"
                visibleFrom='xs'
              >
                {badge}
              </Badge>
              <Badge
                variant="default"
                p="md"
                bg="var(--mantine-color-pink-5)"
                c="var(--mantine-color-white)"
                size="sm"
                mb="lg"
                style={{ textTransform: 'none', border: 'none' }}
                hiddenFrom="xs"
              >
                {badge}
              </Badge>
            </motion.div>
          )}
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
                rightSection=<IconArrowRight />
              >
                Join now!
              </Button>
            </Link>
          </motion.div>
        </Stack>
      </Flex>
    </Container>
  </Container>
);
