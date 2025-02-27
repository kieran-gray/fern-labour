import '@mantine/core/styles.css';

import { useEffect, useState } from 'react';
import type { AppProps } from 'next/app';
import { Quicksand } from 'next/font/google';
import Head from 'next/head';
import type { Container } from '@tsparticles/engine';
import Particles, { initParticlesEngine } from '@tsparticles/react';
import { loadSlim } from '@tsparticles/slim';
import { MantineProvider } from '@mantine/core';
import { theme } from '../theme';

const quicksand = Quicksand({ subsets: ['latin'] });

export default function App({ Component, pageProps }: AppProps) {
  const [init, setInit] = useState(false);

  useEffect(() => {
    initParticlesEngine(async (engine) => {
      await loadSlim(engine);
    }).then(() => {
      setInit(true);
    });
  }, []);

  const particlesLoaded = async (container?: Container | undefined) => {
    console.log(container); // eslint-disable-line no-console
  };

  return (
    <MantineProvider theme={theme}>
      <Head>
        <title>Fern Labour</title>
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width, user-scalable=no"
        />
        <meta
          name="description"
          content="Fern Labour: Plan your labour, Track your Contractions, and keep friends and family up-to-date in one app"
        />
        <link rel="shortcut icon" href="/logo/logo.svg" />
      </Head>
      {init && (
        <Particles
          particlesLoaded={particlesLoaded}
          options={{
            particles: {
              number: { value: 25, density: { enable: true } },
              color: { value: '#ff7964' },
              shape: { type: 'circle' },
              opacity: {
                value: 0.15,
              },
              size: {
                value: 125,
              },
              line_linked: {
                enable: true,
                distance: 150,
                color: '#ffffff',
                opacity: 0.4,
                width: 1,
              },
              move: {
                enable: true,
                speed: 0.5,
                direction: 'none',
                random: false,
                straight: false,
                attract: { enable: false },
              },
            },
            interactivity: {
              events: {
                onHover: { enable: true, mode: 'bubble' },
                onClick: { enable: true, mode: 'repulse' },
              },
              modes: {
                grab: { distance: 400, line_linked: { opacity: 1 } },
                bubble: { distance: 300, size: 100, duration: 5, opacity: 1, speed: 0.1 },
                repulse: { distance: 200, duration: 0.4 },
                push: { particles_nb: 4 },
                remove: { particles_nb: 2 },
              },
            },
            retina_detect: true,
          }}
        />
      )}
      <main className={quicksand.className}>
        <Component {...pageProps} />
      </main>
    </MantineProvider>
  );
}
