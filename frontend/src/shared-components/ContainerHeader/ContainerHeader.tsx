import { Title } from '@mantine/core';
import baseClasses from '../shared-styles.module.css';

export function ContainerHeader({ title }: { title: string }) {
  return (
    <div className={baseClasses.header}>
      <Title fz="xl" className={baseClasses.title}>
        {title}
      </Title>
    </div>
  );
}
