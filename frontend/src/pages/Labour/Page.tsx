import { Header } from '../../shared-components/Header/Header';
import LabourContainer from './Components/LabourContainer/LabourContainer';
import { Center, Space } from '@mantine/core';


export const LabourPage = () => {
    const page = 'Labour';

    return (
        <>
        <Header active={page}/>
        <Center flex={"shrink"} p={15}>
            <LabourContainer />
        </Center>
        <Space h="xl"></Space>
        </>
    )
};
