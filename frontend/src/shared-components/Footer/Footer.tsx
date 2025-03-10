import { useNavigate } from 'react-router-dom';
import { Anchor, Container, Group } from '@mantine/core';
import classes from './Footer.module.css';

const links = [
  { link: '/contact', label: 'Contact' },
  { link: 'https://fernlabour.com/privacy', label: 'Privacy Policy' },
  { link: 'https://fernlabour.com/terms-of-service', label: 'Terms of Service' },
];

export function FooterSimple() {
  const navigate = useNavigate();
  const items = links.map((link) => (
    <Anchor<'a'>
      key={link.label}
      href={link.link}
      onClick={(event) => {
        event.preventDefault();
        if (link.link.startsWith('https://')) {
          window.open(link.link, '_blank')?.focus();
        } else {
          navigate(link.link);
        }
      }}
      size="sm"
    >
      {link.label}
    </Anchor>
  ));

  return (
    <div className={classes.footer}>
      <Container className={classes.inner}>
        <div onClick={() => navigate('/')}>
          <img src="/logo/logo.svg" className={classes.icon} alt="Fern Logo" />
        </div>
        <Group className={classes.links}>{items}</Group>
      </Container>
    </div>
  );
}
