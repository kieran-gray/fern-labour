import { Route, Routes } from 'react-router-dom';
import { SilentRedirect } from './auth/SilentRedirect';
import { appRoutes } from './constants.ts';
import { CompletedLabourPage } from './pages/CompletedLabour/Page.tsx';
import { ContactPage } from './pages/Contact/Page.tsx';
import { HomePage } from './pages/Home/Page.tsx';
import { LabourHistoryPage } from './pages/LabourHistory/Page.tsx';
import { NotFoundPage } from './pages/NotFound/Page.tsx';
import { OnboardingPage } from './pages/Onboarding/Onboarding.tsx';
import { SubscribePage } from './pages/Subscribe/Page.tsx';

export function Router() {
  return (
    <Routes>
      <Route path={appRoutes.SilentRedirect} element={<SilentRedirect />} />
      <Route path={appRoutes.home}>
        <Route index path={appRoutes.home} element={<HomePage />} />
        <Route path={appRoutes.history} element={<LabourHistoryPage />} />
        <Route path={appRoutes.onboarding} element={<OnboardingPage />} />
        <Route path={appRoutes.notFound} element={<NotFoundPage />} />
        <Route path={appRoutes.contact} element={<ContactPage />} />
        <Route path={appRoutes.subscribe} element={<SubscribePage />} />
        <Route path={appRoutes.completed} element={<CompletedLabourPage />} />
      </Route>
    </Routes>
  );
}
