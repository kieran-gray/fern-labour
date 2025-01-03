import { createTheme, MantineColorsTuple } from '@mantine/core';

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
  '#b12500'
];

// https://mantine.dev/colors-generator/?color=FF8C7A
const pinkTheme: MantineColorsTuple = [
    "#ffeae6",
    "#ffd5cd",
    "#ffa99b",
    "#ff7964",
    "#fe5236",
    "#fe3919",
    "#ff2a09",
    "#e41d00",
    "#cb1500",
    "#b20600"
]

export const theme = createTheme({
  fontFamily: 'Quicksand, sans-serif',
  headings: {fontFamily: 'Quicksand'},
  primaryColor: "pink",
  colors: {
    "peach": peachTheme,
    "pink": pinkTheme
  }
});
