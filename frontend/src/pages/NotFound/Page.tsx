import { FooterSimple } from '../../shared-components/Footer/Footer';
import { Header } from '../../shared-components/Header/Header';
import { NotFoundImage } from './Components/Image/Image';

export const NotFoundPage: React.FC = () => {
  return (
    <div style={{ height: '100svh', display: 'flex', flexDirection: 'column' }}>
      <Header active="" />
      <NotFoundImage />
      <div style={{ flexGrow: 1 }} />
      <FooterSimple />
    </div>
  );
};
