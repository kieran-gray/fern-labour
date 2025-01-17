import { Button } from "@mantine/core";
import { IconSend } from "@tabler/icons-react";


export function SendInviteButton() {
    return (
        <Button
            color='var(--mantine-color-pink-4)'
            variant="filled"
            rightSection={
            <IconSend size={20} stroke={1.5} />
            }
            radius="xl"
            size="md"
            pr={14}
            h={48}
            mt={'var(--mantine-spacing-lg)'}
            styles={{ section: { marginLeft: 22 } }}
            type="submit"
        >
            Send invite
        </Button>
    )
}

