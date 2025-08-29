import { Icon } from '@tabler/icons-react';
import { Center, Text } from '@mantine/core';
import classes from './BottomNavigation.module.css';

interface BottomNavItem {
  id: string;
  label: string;
  icon: Icon;
  requiresPaid?: boolean;
}

interface BottomNavigationProps {
  items: readonly BottomNavItem[];
  activeItem: string | null;
  onItemChange: (item: string) => void;
}

export function BottomNavigation({ items, activeItem, onItemChange }: BottomNavigationProps) {
  return (
    <div className={classes.container}>
      <div className={classes.tabsContainer}>
        {items.map(({ id, label, icon: Icon }) => (
          <button
            type="button"
            key={id}
            className={`${classes.tab} ${activeItem === id ? classes.tabActive : ''}`}
            onClick={() => onItemChange(id)}
          >
            <Center className={classes.tabContent}>
              <Icon size={20} className={classes.tabIcon} />
              <Text size="xs" className={classes.tabLabel}>
                {label}
              </Text>
            </Center>
          </button>
        ))}
      </div>
    </div>
  );
}
