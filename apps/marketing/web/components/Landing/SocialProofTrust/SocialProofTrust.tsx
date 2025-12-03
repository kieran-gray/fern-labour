import { IconHeart, IconLock, IconQuote, IconShield, IconStar } from '@tabler/icons-react';
import { motion } from 'motion/react';
import { Box, Container, Group, Stack, Text } from '@mantine/core';

type SocialProofTrustProps = {
  trustTitle: string;
  testimonial: {
    quote: string;
    author: string;
  };
  signals: string[];
};

const iconMap = {
  'NHS-friendly tracking methods': IconHeart,
  'GDPR compliant': IconShield,
  'Secure end-to-end communications': IconLock,
};

export const SocialProofTrust = ({ trustTitle, testimonial, signals }: SocialProofTrustProps) => {
  return (
    <Box bg="white" py={120}>
      <Container size="xl">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: 'easeOut' }}
          viewport={{ once: true }}
        >
          <Stack align="center" gap="xl">
            {/* 1. Trust Title */}
            <Text ta="center" size="lg" fw={500} c="var(--mantine-color-gray-7)">
              {trustTitle}
            </Text>

            {/* 2. Testimonial */}
            <Box ta="center" maw={600}>
              <IconQuote
                size={40}
                color="var(--mantine-color-pink-6)"
                style={{ marginBottom: 20 }}
              />
              <Text size="xl" fw={500} style={{ lineHeight: 1.5 }}>
                "{testimonial.quote}"
              </Text>
              <Text c="var(--mantine-color-gray-7)" mt="md" size="lg">
                — {testimonial.author}
              </Text>

              <Group justify="center" mt="md" gap={4}>
                {[...Array(5)].map((_, i) => (
                  <IconStar
                    key={i}
                    size={16}
                    fill="var(--mantine-color-yellow-5)"
                    color="var(--mantine-color-yellow-5)"
                  />
                ))}
              </Group>
            </Box>

            {/* 3. Trust Icons */}
            <Group justify="center" align="start" gap="xl" mt="xl">
              {signals.map((signal, index) => {
                const IconComponent = iconMap[signal as keyof typeof iconMap] || IconShield;

                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{
                      duration: 0.4,
                      delay: 0.4 + index * 0.1,
                      ease: 'easeOut',
                    }}
                    viewport={{ once: true }}
                  >
                    <Stack align="center" gap="xs" maw={140}>
                      <Box
                        w={60}
                        h={60}
                        style={{
                          borderRadius: '50%',
                          backgroundColor: 'var(--mantine-color-pink-0)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          flexShrink: 0,
                        }}
                      >
                        <IconComponent size={24} color="var(--mantine-color-pink-6)" />
                      </Box>
                      <Text size="sm" ta="center" c="var(--mantine-color-gray-7)" lh={1.3}>
                        {signal}
                      </Text>
                    </Stack>
                  </motion.div>
                );
              })}
            </Group>
          </Stack>
        </motion.div>
      </Container>
    </Box>
  );
};
