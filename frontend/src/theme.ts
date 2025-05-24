import { createTheme, MantineColorsTuple, virtualColor } from '@mantine/core';

// https://mantine.dev/colors-generator/?color=ffa587
const peachTheme: MantineColorsTuple = [
  '#ffeee5',
  '#ffdbce',
  '#ffb49c',
  '#fe8c65',
  '#fe6938',
  '#fe531b',
  '#fe480b',
  '#e33900',
  '#cb3000',
  '#b12500',
];

// https://mantine.dev/colors-generator/?color=FF8C7A
const pinkTheme: MantineColorsTuple = [
  '#ffeae6',
  '#ffd5cd',
  '#ffa99b',
  '#ff7964',
  '#fe5236',
  '#fe3919',
  '#ff2a09',
  '#e41d00',
  '#cb1500',
  '#b20600',
];

const darkTheme: MantineColorsTuple = [
  '#01010a',
  '#0c0d21',
  '#1d1e30',
  '#2b2c3d',
  '#34354a',
  '#4d4f66',
  '#666980',
  '#8c8fa3',
  '#acaebf',
  '#d5d7e0',
];

// Marketing Hightlights: #24968b

export const theme = createTheme({
  fontFamily: 'Quicksand, sans-serif',
  headings: { fontFamily: 'Quicksand' },
  primaryColor: 'pink',
  autoContrast: true,
  colors: {
    peach: peachTheme,
    pink: pinkTheme,
    dark: darkTheme,
    primary: virtualColor({
      name: 'primary',
      dark: 'dark',
      light: 'pink',
    }),
  },
});
