import { createTheme, MantineColorsTuple } from '@mantine/core';

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

export const theme = createTheme({
  fontFamily: 'Quicksand, sans-serif',
  headings: { fontFamily: 'Poppins, sans-serif' },
  primaryColor: 'pink',
  colors: {
    pink: pinkTheme,
  },
});
