import Link from 'next/link';
import { Container, Group } from '@mantine/core';
import classes from './Footer.module.css';

const links = [
  { link: '/contact', label: 'Contact' },
  { link: '/privacy', label: 'Privacy' },
];

export function FooterSimple() {
  const items = links.map((link) => (
    <Link className={classes.link} key={link.label} href={link.link}>
      {link.label}
    </Link>
  ));

  return (
    <div className={classes.footer}>
      <Container className={classes.inner}>
        <Link href="/">
          <img src="/logo/logo.svg" className={classes.icon} alt="Fern Logo" />
        </Link>
        <Group className={classes.links}>{items}</Group>
      </Container>
    </div>
  );
}
