import { Button, Container, Group, Image, List, Text, ThemeIcon, Title } from '@mantine/core';
import classes from './HeroBullets.module.css';
import { IconNumber1, IconNumber2, IconNumber3, IconNumber4 } from '@tabler/icons-react';
import Link from 'next/link';


export function HeroBullets () {
    return (
    <Container size="lg" className={classes.container} id='#home'>
      <div className={classes.inner}>
        <div className={classes.content}>
          <Title className={classes.title}>
            Empowering Your <br /> Labour Journey, Together
          </Title>
          <Text mt="md">
            Track every contraction, share real-time updates, and keep loved ones connected - all in one place.
          </Text>

          <List
            mt={30}
            spacing="sm"
            size="sm"
          >
            <List.Item icon={
              <ThemeIcon size={25} radius="xl">
                <IconNumber1 size={12} stroke={3} />
              </ThemeIcon>
            }>
              <b>Plan Your Labour</b> – Set your due date
            </List.Item>
            <List.Item icon={
              <ThemeIcon size={25} radius="xl">
                <IconNumber2 size={12} stroke={3} />
              </ThemeIcon>
            }>
              <b>Invite friends and family</b> – Share invites to follow your labour by link, email, or QR code.
            </List.Item>
            <List.Item icon={
              <ThemeIcon size={25} radius="xl">
                <IconNumber3 size={12} stroke={3} />
              </ThemeIcon>
            }>
              <b>Track your labour</b> – Track your contractions and get to the hospital on time
            </List.Item>
            <List.Item icon={
              <ThemeIcon size={25} radius="xl">
                <IconNumber4 size={12} stroke={3} />
              </ThemeIcon>
            }>
              <b>Automatic notifications</b> – Friends and Family are notified when you start labour and you can keep them updated with announcements
            </List.Item>
          </List>

          <Group mt={30}>
            <Link href='https://track.fernlabour.com' target='_blank'>
              <Button radius="xl" size="md" className={classes.control}>
                Join now!
              </Button>
            </Link>
            <Button 
              variant="default"
              radius="xl"
              size="md"
              className={classes.control}
              onClick={(event) => {
                event.preventDefault();
                const element = document.getElementById('#features');
                const headerOffset = 100;
                const elementPos = element!.getBoundingClientRect().top;
                const offsetPos = elementPos + window.scrollY - headerOffset;
                window.scrollTo({top: offsetPos, behavior: 'smooth'});
            }}
              >
               Tell me more
            </Button>
          </Group>
        </div>
        <Image src='images/Hero.png' className={classes.image} />
      </div>
    </Container>
    )
}

