import { IconAt, IconBrandInstagram } from '@tabler/icons-react';
import { ActionIcon, Box, Stack, Text } from '@mantine/core';
import classes from './ContactIcons.module.css';

interface ContactIconProps extends Omit<React.ComponentPropsWithoutRef<'div'>, 'title'> {
  icon: typeof IconAt;
  title: React.ReactNode;
  description: React.ReactNode;
  link: string | null | undefined;
}

function ContactIcon({ icon: Icon, title, description, link, ...others }: ContactIconProps) {
  return (
    <div className={classes.wrapper} {...others}>
      <Box mr="md">
        {(link != null && (
          <ActionIcon
            target="_blank"
            component="a"
            href={link}
            size={28}
            className={classes.social}
            c="var(--mantine-color-gray-8)"
            variant="transparent"
          >
            <Icon size={24} color="var(--mantine-color-gray-8)" />
          </ActionIcon>
        )) || <Icon size={24} color="var(--mantine-color-gray-8)" />}
      </Box>

      <div>
        <Text size="xs">{title}</Text>
        <Text size="md" visibleFrom="sm">
          {description}
        </Text>
        <Text size="sm" hiddenFrom="sm">
          {description}
        </Text>
      </div>
    </div>
  );
}

const data = [
  { title: 'Email', description: 'support@fernlabour.com', icon: IconAt, link: undefined },
  {
    title: 'Instagram',
    description: 'fernlabour',
    icon: IconBrandInstagram,
    link: 'https://www.instagram.com/fernlabour/',
  },
];

export function ContactIconsList() {
  const items = data.map((item, index) => <ContactIcon key={index} {...item} />);
  return <Stack>{items}</Stack>;
}
