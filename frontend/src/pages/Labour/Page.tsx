import { Center, Space } from '@mantine/core';
import { FooterSimple } from '../../shared-components/Footer/Footer';
import { Header } from '../../shared-components/Header/Header';
import LabourContainer from './Components/LabourContainer/LabourContainer';

export const LabourPage = () => {
  const page = 'Labour';

  return (
    <div style={{ height: '100svh', display: 'flex', flexDirection: 'column' }}>
      <Header active={page} />
      <Center flex="shrink" p={15}>
        <LabourContainer />
      </Center>
      <Space h="xl" />
      <div style={{ flexGrow: 1 }} />
      <FooterSimple />
    </div>
  );
};
