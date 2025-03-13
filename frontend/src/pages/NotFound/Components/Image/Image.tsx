import { useNavigate } from 'react-router-dom';
import { Button, Image, Text, Title } from '@mantine/core';
import image from './notFound.svg';
import baseClasses from '../../../../shared-components/shared-styles.module.css';
import classes from './Image.module.css';

export function NotFoundImage() {
  const navigate = useNavigate();
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner} style={{ width: '100%' }}>
          <div style={{ justifyContent: 'space-between' }}>
            <Title order={2} visibleFrom="sm">
              We're not sure how you got here...
            </Title>
            <Title order={3} hiddenFrom="sm">
              We're not sure how you got here...
            </Title>
            <div className={classes.imageFlexRow}>
              <Image src={image} className={classes.mobileImage} />
            </div>
            <Text c="var(--mantine-color-gray-8)" size="lg" mt="30">
              The page you are trying to open does not exist. You may have mistyped the address, or
              the page has been moved to another URL. If you think this is an error contact support.
            </Text>
            <Button
              variant="outline"
              size="md"
              mt="xl"
              radius="xl"
              className={classes.control}
              onClick={() => {
                navigate('/');
              }}
            >
              Lets take you home
            </Button>
          </div>
          <Image src={image} className={classes.desktopImage} />
        </div>
      </div>
    </div>
  );
}
