import { Accordion, Container, Grid, Image, List, Text, Title } from '@mantine/core';
import classes from './FaqWithImage.module.css';

export function FaqWithImage() {
  return (
    <Container pt={40} pb={120} px="15px" fluid>
      <Container size="lg" className={classes.container} id="#faqs">
        <Grid id="faq-grid" gutter={50}>
          <Grid.Col span={{ base: 12, sm: 6 }}>
            <Image src="images/FAQ.svg" className={classes.bigImage} alt="Question mark" />
          </Grid.Col>
          <Grid.Col span={{ base: 12, md: 6 }}>
            <Title order={1} ta="left" className={classes.title}>
              Frequently Asked Questions
            </Title>

            <Accordion
              chevronPosition="right"
              variant="separated"
              classNames={{ control: classes.control, panel: classes.panel, item: classes.item }}
            >
              <Accordion.Item className={classes.item} value="hospital">
                <Accordion.Control>How will I know when to go to hospital?</Accordion.Control>
                <Accordion.Panel>
                  <Text>
                    The app monitors your contraction patterns and recommends next steps based on
                    your labour history. Here are the general guidelines:
                  </Text>

                  <div className={classes.adviceCard}>
                    <Text className={classes.adviceTitle}>First-time mothers</Text>
                    <Text>
                      We recommend going to hospital when your contractions follow a
                      <b> 3-1-1</b> pattern: every 3 minutes, lasting 1 minute, for 1 hour.
                    </Text>
                  </div>

                  <div className={classes.adviceCard}>
                    <Text className={classes.adviceTitle}>Have given birth before</Text>
                    <Text>
                      We recommend going to hospital when your contractions follow a
                      <b> 5-1-1</b> pattern: every 5 minutes, lasting 1 minute, for 1 hour.
                    </Text>
                  </div>

                  <Text className={classes.note}>
                    Always follow the specific guidance of your healthcare provider, as your
                    individual situation may differ.
                  </Text>
                </Accordion.Panel>
              </Accordion.Item>

              <Accordion.Item className={classes.item} value="subscribe">
                <Accordion.Control>Can I control who subscribes to my labour?</Accordion.Control>
                <Accordion.Panel>
                  <List spacing="xs" className={classes.panelText}>
                    <List.Item>
                      You approve each person who requests to join your labour circle.
                    </List.Item>
                    <List.Item>
                      You can remove or block subscribers at any time in
                      <b> Manage Subscribers</b>, changes apply immediately.
                    </List.Item>
                  </List>
                </Accordion.Panel>
              </Accordion.Item>

              <Accordion.Item className={classes.item} value="data">
                <Accordion.Control>How will my data be stored?</Accordion.Control>
                <Accordion.Panel>
                  <List spacing="xs" className={classes.panelText}>
                    <List.Item>
                      Your personal information is encrypted and stored on secure servers in the
                      United Kingdom.
                    </List.Item>
                    <List.Item>
                      We use industry‑standard SSL encryption for all data transmission and encrypt
                      identifying information at rest.
                    </List.Item>
                    <List.Item>You can request to delete your data at any time.</List.Item>
                  </List>
                </Accordion.Panel>
              </Accordion.Item>

              <Accordion.Item className={classes.item} value="subscribers">
                <Accordion.Control>
                  Is there a limit to how many people can subscribe to my labour?
                </Accordion.Control>
                <Accordion.Panel>
                  <Text className={classes.panelText}>
                    There’s no limit, invite as many loved ones as you like.
                  </Text>
                </Accordion.Panel>
              </Accordion.Item>
            </Accordion>
          </Grid.Col>
        </Grid>
      </Container>
    </Container>
  );
}
