import { IconPlus } from '@tabler/icons-react';
import { Accordion, Container, ThemeIcon, Title } from '@mantine/core';
import classes from './FaqSimple.module.css';

export function FaqSimple() {
  return (
    <Container size="lg" mt={20} className={classes.wrapper} id="#faqs">
      <Title ta="center" className={classes.title}>
        Frequently Asked Questions
      </Title>

      <Accordion
        chevronPosition="right"
        chevronSize={26}
        variant="separated"
        disableChevronRotation
        styles={{ label: { color: 'var(--mantine-color-black)' }, item: { border: 0 } }}
        chevron={
          <ThemeIcon radius="xl" className={classes.gradient} size={26}>
            <IconPlus size={18} stroke={1.5} />
          </ThemeIcon>
        }
      >
        <Accordion.Item className={classes.item} value="hospital">
          <Accordion.Control>How will I know when to go to hospital?</Accordion.Control>
          <Accordion.Panel className={classes.panel}>
            The app will monitor your contraction patterns and send you a recommendation based on
            your labour history.
            <br />
            For first-time mothers, you'll receive a notification when your contractions follow a
            3-1-1 pattern (contractions every 3 minutes, lasting 1 minute, for 1 hour).
            <br />
            For those who have given birth before, you'll be notified at a 5-1-1 pattern
            (contractions every 5 minutes, lasting 1 minute, for 1 hour).
            <br />
            However, always follow your healthcare provider's specific guidance, as they may give
            you different instructions based on your individual situation.
          </Accordion.Panel>
        </Accordion.Item>

        <Accordion.Item className={classes.item} value="remove-subs">
          <Accordion.Control>
            Can I remove subscribers from my labour if I don't want them to follow?
          </Accordion.Control>
          <Accordion.Panel className={classes.panel}>
            Yes, absolutely. You have complete control over who receives updates. You can remove any
            subscriber at any time through the app's settings, and they'll immediately stop
            receiving notifications.
          </Accordion.Panel>
        </Accordion.Item>

        <Accordion.Item className={classes.item} value="data-storage">
          <Accordion.Control>How will my data be stored?</Accordion.Control>
          <Accordion.Panel className={classes.panel}>
            Your privacy and data security are our top priority. All your personal information is
            encrypted and stored on secure servers located in Europe.
            <br />
            We use industry-standard SSL encryption for all data transmission, and your identifying
            information is encrypted when stored.
            <br />
            You can request to delete your data at any time through the app.
          </Accordion.Panel>
        </Accordion.Item>

        <Accordion.Item className={classes.item} value="partner-updates">
          <Accordion.Control>
            Can my partner/support person help manage updates during labor?
          </Accordion.Control>
          <Accordion.Panel className={classes.panel}>
            Yes! You can designate a trusted support person to manage updates through the app while
            you focus on your labor.
            <br />
            They can track contractions and send updates to your subscribers using their own device
            - just share your unique access code with them.
            <br />
            You maintain full control and can revoke access at any time.
          </Accordion.Panel>
        </Accordion.Item>

        <Accordion.Item className={classes.item} value="sub-limits">
          <Accordion.Control>
            Is there a limit to how many people can subscribe to my updates?
          </Accordion.Control>
          <Accordion.Panel className={classes.panel}>
            No, there's no limit to the number of subscribers you can add. Whether you want to keep
            just immediate family updated or include your extended support network, the platform can
            handle it.
          </Accordion.Panel>
        </Accordion.Item>
      </Accordion>
    </Container>
  );
}
