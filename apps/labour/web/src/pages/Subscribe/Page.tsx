import { AppMode, useLabourSession } from '@base/contexts';
import { useLabourV2Client, useRequestAccessV2 } from '@base/hooks';
import { AppShell } from '@shared/AppShell';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { Button, Group, Image, PinInput, Space, Text, Title } from '@mantine/core';
import { useForm } from '@mantine/form';
import image from './protected.svg';
import classes from './Form.module.css';
import baseClasses from '@shared/shared-styles.module.css';

const SUBSCRIBER_TOKEN_LENGTH = 5;

export const SubscribePage: React.FC = () => {
  const { id } = useParams<'id'>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { setMode } = useLabourSession();
  const token = searchParams.get('token');
  if (!id) {
    throw new Error('id is required');
  }

  const labourId = id;

  const form = useForm({
    mode: 'uncontrolled',
    initialValues: {
      token: token || '',
    },
    validate: {
      token: (value) => (value.length !== SUBSCRIBER_TOKEN_LENGTH ? 'Invalid token' : null),
    },
  });

  const client = useLabourV2Client();
  const mutation = useRequestAccessV2(client);

  const handleSubscribeTo = (values: typeof form.values) => {
    const requestBody = { labourId, token: values.token };
    mutation.mutate(requestBody, {
      onSuccess: () => {
        setMode(AppMode.Subscriber);
        navigate(`/?prompt=requested`);
      },
    });
  };

  return (
    <AppShell>
      <div className={baseClasses.flexPageColumn}>
        <div className={baseClasses.root}>
          <div className={baseClasses.body}>
            <div className={baseClasses.inner}>
              <div className={classes.content}>
                <Title className={classes.title}>
                  Congratulations! <br /> Someone wants to share their labour journey with you!
                </Title>
                <div className={baseClasses.imageFlexRow}>
                  <Image src={image} className={baseClasses.smallImage} />
                </div>
                <Text className={baseClasses.description} mt="md">
                  If the code isn't already filled in, check the share message that was sent to you,
                  or ask the person who shared the link with you for the code.
                </Text>
                <Group mt={30}>
                  <form
                    onSubmit={form.onSubmit((values) => handleSubscribeTo(values))}
                    className={classes.form}
                  >
                    <div className={baseClasses.flexRowEnd}>
                      <PinInput
                        fw={600}
                        size="lg"
                        length={SUBSCRIBER_TOKEN_LENGTH}
                        radius="md"
                        style={{ justifyContent: 'center' }}
                        styles={{
                          input: {
                            color:
                              'light-dark(var(--mantine-color-black), var(--mantine-color-gray-1))',
                          },
                        }}
                        key={form.key('token')}
                        {...form.getInputProps('token')}
                      />
                      <Space w="xl" h="xl" />
                      <Button
                        size="lg"
                        radius="lg"
                        variant="filled"
                        type="submit"
                        loading={mutation.isPending}
                      >
                        Submit
                      </Button>
                    </div>
                  </form>
                </Group>
              </div>
              <Image src={image} className={classes.image} />
            </div>
          </div>
        </div>
      </div>
    </AppShell>
  );
};
