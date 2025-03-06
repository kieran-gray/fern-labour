import { IconArrowUp } from '@tabler/icons-react';
import { Affix, Button, Transition } from '@mantine/core';
import { useWindowScroll } from '@mantine/hooks';
import { PrivacyPolicy } from './PrivacyPolicy';

export const PrivacyPageContent = () => {
  const [scroll, scrollTo] = useWindowScroll();

  return (
    <>
      <div style={{ padding: '15px' }}>
        <PrivacyPolicy />
        <Affix position={{ bottom: 20, right: 20 }}>
          <Transition transition="slide-up" mounted={scroll.y > 0}>
            {(transitionStyles) => (
              <Button
                leftSection={<IconArrowUp size={16} />}
                style={transitionStyles}
                onClick={() => scrollTo({ y: 0 })}
                bg={'var(--mantine-color-pink-4)'}
                radius="lg"
              >
                Scroll to top
              </Button>
            )}
          </Transition>
        </Affix>
      </div>
      <div style={{ flexGrow: 1 }} />
    </>
  );
};
