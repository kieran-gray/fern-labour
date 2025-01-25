import '@mantine/core/styles.css';

import type { AppProps } from 'next/app';
import Head from 'next/head';
import { MantineProvider } from '@mantine/core';
import { theme } from '../theme';
import { Bubbles } from '@/components/Bubbles/Bubbles';
import { Quicksand } from 'next/font/google'

const quicksand = Quicksand({subsets: ["latin"]})

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
      </Head>
      <Bubbles />
      <main className={quicksand.className}>
        <Component {...pageProps} />
      </main>
    </MantineProvider>
  );
}
