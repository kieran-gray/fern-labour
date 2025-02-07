import { Route, Routes } from 'react-router-dom';
import { appRoutes } from './constants.ts';
import { ContactPage } from './pages/Contact/Page.tsx';
import { LabourPage } from './pages/Labour/Page.tsx';
import { NotFoundPage } from './pages/NotFound/Page.tsx';
import { ShareBirthingPersonPage } from './pages/Share/Page.tsx';
import { SubscribePage } from './pages/Subscribe/Page.tsx';
import { TrackPage } from './pages/Track/Page.tsx';

export function Router() {
  return (
    <Routes>
      <Route path={appRoutes.track}>
        <Route index path={appRoutes.track} element={<TrackPage />} />
        <Route path={appRoutes.notFound} element={<NotFoundPage />} />
        <Route path={appRoutes.share} element={<ShareBirthingPersonPage />} />
        <Route path={appRoutes.labour} element={<LabourPage />} />
        <Route path={appRoutes.contact} element={<ContactPage />} />
        <Route path={appRoutes.subscribe} element={<SubscribePage />} />
      </Route>
    </Routes>
  );
}
