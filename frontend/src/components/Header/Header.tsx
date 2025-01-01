import { Anchor, Box, Burger, Container, Group } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import classes from './Header.module.css';
import { useNavigate } from "react-router-dom";
import { useAuth } from 'react-oidc-context';

const mainLinks = [
    { link: '/', label: 'Home' },
    { link: '/labour', label: 'Labour' },
    { link: '/share', label: 'Share' },

];

export function Header({active}: {active: string}) {
    const [opened, { toggle }] = useDisclosure(false);
    const navigate = useNavigate();
    const auth = useAuth()

    const mainItems = mainLinks.map((item) => (
        <Anchor<'a'>
            href={item.link}
            key={item.label}
            className={classes.mainLink}
            data-active={item.label === active || undefined}
            onClick={(event) => {
                event.preventDefault();
                navigate(item.link)
            }}
        >
            {item.label}
        </Anchor>
    ));
    const logout = (
        <Anchor<'a'>
            key={'Logout'}
            className={classes.mainLink}
            onClick={() => {
                void auth.signoutRedirect();
            }}
        >
            Logout
        </Anchor>
    )
    return (
        <header className={classes.header} color='peach'>
            <Container className={classes.inner}>
                <Box className={classes.links} visibleFrom="sm">
                    <Group gap={30} justify="flex-end" className={classes.mainLinks}>
                        {mainItems}
                    </Group>
                </Box>
                <Group visibleFrom='sm'>
                        {logout}
                    </Group>
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