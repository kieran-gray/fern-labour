import { Accordion, Container, Grid, Image, Title } from '@mantine/core';
import classes from './FaqWithImage.module.css';

export function FaqWithImage() {
  return (
    <Container py="calc(var(--mantine-spacing-lg) * 3)" px="15px" fluid>
      <Container size="lg" className={classes.container} id="#faqs">
        <Grid id="faq-grid" gutter={50}>
          <Grid.Col span={{ base: 12, sm: 6 }}>
            <Image src="images/FAQ.svg" className={classes.bigImage} alt="Question mark" />
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 6 }}>
            <Title order={1} ta="left" className={classes.title}>
              Frequently Asked Questions
            </Title>

            <Accordion chevronPosition="right" variant="separated">
              <Accordion.Item className={classes.item} value="hospital">
                <Accordion.Control>How will I know when to go to hospital?</Accordion.Control>
                <Accordion.Panel>
                  The app will monitor your contraction patterns and send you a recommendation based
                  on your labour history.
                  <br />
                  For first-time mothers, you'll receive a notification when your contractions
                  follow a 3-1-1 pattern (contractions every 3 minutes, lasting 1 minute, for 1
                  hour).
                  <br />
                  For those who have given birth before, you'll be notified at a 5-1-1 pattern
                  (contractions every 5 minutes, lasting 1 minute, for 1 hour).
                  <br />
                  However, always follow your healthcare provider's specific guidance, as they may
                  give you different instructions based on your individual situation.
                </Accordion.Panel>
              </Accordion.Item>

              <Accordion.Item className={classes.item} value="subscribe">
                <Accordion.Control>Can I control who subscribes to my labour?</Accordion.Control>
                <Accordion.Panel>
                  Yes, absolutely. You have complete control over who receives updates. You need to
                  approve anyone who requests to join your labour circle.
                  <br />
                  Additionally, you can remove or block any subscriber at any time through the
                  "Manage Subscribers" controls in the app, and they'll immediately be removed.
                </Accordion.Panel>
              </Accordion.Item>

              <Accordion.Item className={classes.item} value="data">
                <Accordion.Control>How will my data be stored?</Accordion.Control>
                <Accordion.Panel>
                  Your privacy and data security are our top priority. All your personal information
                  is encrypted and stored on secure servers located in the United Kingdom.
                  <br />
                  We use industry-standard SSL encryption for all data transmission, and your
                  identifying information is encrypted when stored.
                  <br />
                  You can request to delete your data at any time through the app.
                </Accordion.Panel>
              </Accordion.Item>

              {/* <Accordion.Item className={classes.item} value="birth-partner">
                <Accordion.Control>
                  Can my birth partner help manage updates during labour?
                </Accordion.Control>
                <Accordion.Panel>
                  Yes! With an Advanced plan (see above), you can designate a trusted support person
                  to manage updates through the app while you focus on your labour.
                  <br />
                  They can track contractions and send updates to your subscribers using their own
                  device.
                  <br />
                  You maintain full control and can revoke access at any time.
                </Accordion.Panel>
              </Accordion.Item> */}

              <Accordion.Item className={classes.item} value="subscribers">
                <Accordion.Control>
                  Is there a limit to how many people can subscribe to my labour?
                </Accordion.Control>
                <Accordion.Panel>
                  There are no limits, you can invite as many loved ones as you want to join in your
                  labour journey.
                </Accordion.Panel>
              </Accordion.Item>
            </Accordion>
          </Grid.Col>
        </Grid>
      </Container>
    </Container>
  );
}
