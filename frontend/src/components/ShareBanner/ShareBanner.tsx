import { Text, Title } from '@mantine/core';
import classes from './ShareBanner.module.css';
import baseClasses from '../shared-styles.module.css'
import { CopyButton } from '../Buttons/CopyButton/CopyButton';


export const ShareBanner = ({ userId, token, copyText }: { userId: string, token: string, copyText: string }) => (
  <div className={baseClasses.root}>
    <div className={baseClasses.header}>
      <Title fz="xl" className={baseClasses.title}>Share</Title>
    </div>
    <div className={baseClasses.body}>
      <Text className={baseClasses.text}>Share this link with friends and family to allow them to track your labour:</Text>
      <div className={classes.share}>
        <Text fw={500} fz="md" mb={5}>
          Hey, follow this link and sign up to get notifications about my labour:
          <br></br>
          <br></br>
          https://fernlabour.com/subscribe/{userId}
        </Text>
        <Text fz="sm">
          <br></br>
          You'll also need this code: <strong>{token}</strong>
        </Text>
      </div>
      <div className={classes.controls}>
        <CopyButton text={copyText} />
      </div>
    </div>
  </div>
);

