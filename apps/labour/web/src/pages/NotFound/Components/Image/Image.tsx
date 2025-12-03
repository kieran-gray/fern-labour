import { ResponsiveDescription } from '@shared/ResponsiveDescription/ResponsiveDescription';
import { ResponsiveTitle } from '@shared/ResponsiveTitle/ResponsiveTitle';
import { useNavigate } from 'react-router-dom';
import { Button, Image } from '@mantine/core';
import image from './notFound.svg';
import classes from './Image.module.css';
import baseClasses from '@shared/shared-styles.module.css';

export function NotFoundImage() {
  const navigate = useNavigate();
  const title = "We're not sure how you got here...";
  const description =
    'The page you are trying to open does not exist. You may have mistyped the address, or the page has been moved to another URL. If you think this is an error contact support.';
  return (
    <div className={baseClasses.root}>
      <div className={baseClasses.body}>
        <div className={baseClasses.inner} style={{ width: '100%' }}>
          <div style={{ justifyContent: 'space-between' }}>
            <ResponsiveTitle title={title} />
            <div className={classes.imageFlexRow}>
              <Image src={image} className={classes.mobileImage} />
            </div>
            <ResponsiveDescription description={description} marginTop={30} />
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
