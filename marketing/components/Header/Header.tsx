import { Box, Burger, Container, Drawer, Group, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import classes from './Header.module.css';
import Link from 'next/link';

const mainLinks = [
    { link: '#home', label: 'Home'},
    { link: '#features', label: 'Features'},
    { link: '#faqs', label: 'FAQs' },
];

export function Header({page}: {page: string}) {
    const [opened, { toggle }] = useDisclosure(false);

    const mainItems = page === 'home' ? mainLinks.map((item) => (
        <Link
            href={item.link}
            key={item.label}
            className={classes.mainLink}
            onClick={(event) => {
                event.preventDefault();
                const element = document.getElementById(item.link);
                const headerOffset = 100;
                const elementPos = element!.getBoundingClientRect().top;
                const offsetPos = elementPos + window.scrollY - headerOffset;
                window.scrollTo({top: offsetPos, behavior: 'smooth'});
                if (opened) toggle()
            }}
        >
            {item.label}
        </Link>
    )): [];

    const goToApp = (
        <Link
            href='https://track.fernlabour.com'
            key={'GoToApp'}
            className={classes.mainLink}
            target="_blank"
        >
            Go to App
        </Link>
    )
    return (
        <header className={classes.header}>
            <Container className={classes.inner}>
                <Link href="/" className={classes.titleRow}>
                    <img src="/logo/logo.svg" className={classes.icon}></img>
                    <Text className={classes.title} >Fern Labour</Text>
                </Link>
                <Box className={classes.links} visibleFrom="sm">
                    <Group gap={30} justify="flex-end" className={classes.mainLinks}>
                        {mainItems}
                    </Group>
                </Box>
                <Group visibleFrom='sm'>
                        {goToApp}
                </Group>
                <Drawer size="xs" classNames={{content: classes.drawer, header: classes.drawer}} overlayProps={{ backgroundOpacity: 0.55, blur: 3 }} position="right" opened={opened} onClose={toggle}>
                    <div className={classes.linksDrawer}>
                        {mainItems}
                        {goToApp}
                    </div>  
                </Drawer>
                <Burger
                    opened={opened}
                    onClick={toggle}
                    className={classes.burger}
                    size="sm"
                    hiddenFrom="sm"
                />
            </Container>
        </header>
    );
}