import { Route, Routes } from 'react-router-dom';
import { appRoutes } from './constants.ts';
import { ContactPage } from './pages/Contact/Page.tsx';
import { LabourPage } from './pages/Labour/Page.tsx';
import { NotFoundPage } from './pages/NotFound/Page.tsx';
import { SubscribePage } from './pages/Subscribe/Page.tsx';

export function Router() {
  return (
    <Routes>
      <Route path={appRoutes.labour}>
        <Route index path={appRoutes.labour} element={<LabourPage />} />
        <Route path={appRoutes.notFound} element={<NotFoundPage />} />
        <Route path={appRoutes.contact} element={<ContactPage />} />
        <Route path={appRoutes.subscribe} element={<SubscribePage />} />
      </Route>
    </Routes>
  );
}
