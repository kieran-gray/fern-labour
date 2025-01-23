import { FooterSimple } from '../../shared-components/Footer/Footer';
import { Header } from '../../shared-components/Header/Header';
import LabourContainer from './Components/LabourContainer/LabourContainer';
import { Center, Space } from '@mantine/core';


export const LabourPage = () => {
    const page = 'Labour';

    return (
        <div style={{ height: '100svh', display: 'flex', flexDirection: 'column' }}>
            <Header active={page} />
            <Center flex={"shrink"} p={15}>
                <LabourContainer />
            </Center>
            <Space h="xl"></Space>
            <div style={{ flexGrow: 1 }}></div>
            <FooterSimple />
        </div>
    )
};
