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
  '#121212',
  '#1e1e1e',
  '#282828',
  '#333333',
  '#3f3f3f',
  '#4b4b4b',
  '#575757',
  '#646464',
  '#717171',
  '#7e7e7e',
];

// Marketing Hightlights: #24968b

export const theme = createTheme({
  fontFamily: 'Quicksand, sans-serif',
  headings: { fontFamily: 'Poppins, sans-serif' },
  primaryColor: 'pink',
  primaryShade: { light: 6, dark: 4 },
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
