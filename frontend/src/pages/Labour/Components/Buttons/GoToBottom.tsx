import { Button } from '@mantine/core';

export default function GoToBottomButton() {
    return <Button 
        radius="lg"
        size='md'
        variant="outline"
        style={{position: "absolute"}}
        onClick={() => window.scrollTo(0, document.body.scrollHeight)}
        >
            ↓
    </Button>;
}