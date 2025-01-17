import { Text, TextInput, Title } from '@mantine/core';
import baseClasses from '../../../../shared-components/shared-styles.module.css'
import { IconAt } from '@tabler/icons-react';
import { SendInviteButton } from '../SendInviteButton/SendInviteButton';
import { useForm } from '@mantine/form';
import { notifications } from '@mantine/notifications';

export function InviteContainer() {
    const form = useForm({
        mode: 'uncontrolled',
        initialValues: {
          email: '',
        },
    
        validate: {
          email: (value) => (/^\S+@\S+$/.test(value) ? null : 'Invalid email'),
        },
    });

    const submitInvite = () => {
        notifications.show(
            {
                title: 'Error',
                message: "Not implemented",
                radius: "lg",
                color: "var(--mantine-color-pink-9)",
                classNames: {
                    title: baseClasses.notificationTitle,
                    description: baseClasses.notificationDescription
                },
                style:{ backgroundColor: "var(--mantine-color-pink-4)", color: "var(--mantine-color-white)" }
            }
        );
    }
      

    return (
        <form onSubmit={form.onSubmit(submitInvite)}>
            <div className={baseClasses.root}>
                <div className={baseClasses.header}>
                    <Title fz="xl" className={baseClasses.title}>Invite</Title>
                </div>
                <div className={baseClasses.body}>
                    <Text className={baseClasses.text}>Invite friends and family to allow them to track your labour:</Text>
                    <TextInput
                        withAsterisk
                        radius={"lg"}
                        mt="md"
                        rightSectionPointerEvents="none"
                        rightSection={<IconAt size={16} />}
                        label="Email"
                        placeholder="friend@email.com"
                        key={form.key('email')}
                        size={"md"}
                        {...form.getInputProps('email')}
                    />
                    <div className={baseClasses.flexRowEnd}>
                        <SendInviteButton />
                    </div>
                </div>
            </div>
        </form>
    )
}
