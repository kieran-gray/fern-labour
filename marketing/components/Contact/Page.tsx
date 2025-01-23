import { FooterSimple } from '@/components/Footer/Footer';
import { Header } from '@/components/Header/Header';
import { ContactUs } from './ContactUs/ContactUs';

export const ContactPage = () => {
    return (
        <>
            <div style={{padding: '15px'}}>
                <ContactUs />
            </div>
            <div style={{flexGrow: 1}}></div>
        </>
    );
};