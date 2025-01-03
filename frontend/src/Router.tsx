import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { HomePage } from './pages/Home/Page.tsx';
import { ShareBirthingPersonPage } from './pages/Share/Page.tsx';
import { LabourPage } from './pages/Labour/Page.tsx'
import { NotFoundPage } from './pages/NotFound/Page.tsx';
import { SubscribePage } from './pages/Subscribe/Page.tsx';


const router = createBrowserRouter([
  {
    path: '/',
    element: <HomePage />,
  },
  {
    path: '/*',
    element: <NotFoundPage />
  },
  {
    path: '/share',
    element: <ShareBirthingPersonPage />
  },
  {
    path: '/labour',
    element: <LabourPage />
  },
  {
    path: '/subscribe/:id',
    element: <SubscribePage />
  }
])


export function Router() {
  return <RouterProvider router={router} />;
}
