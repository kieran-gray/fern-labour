import '@mantine/core/styles.css';

import type { AppProps } from 'next/app';
import Head from 'next/head';
import { MantineProvider } from '@mantine/core';
import { theme } from '../theme';
import { Bubbles } from '@/components/Bubbles/Bubbles';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <MantineProvider theme={theme}>
      <Head>
        <title>Fern Labour</title>
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width, user-scalable=no"
        />
        <link rel="shortcut icon" href="/logo/logo.svg" />
        <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700;1000" rel="stylesheet" />
      </Head>
      <Bubbles />
      <Component {...pageProps} />
    </MantineProvider>
  );
}
