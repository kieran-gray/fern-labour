import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { HomePage } from './pages/Home.tsx';
import { ShareBirthingPersonPage } from './pages/ShareBirthingPerson.tsx';
import { LabourPage } from './pages/Labour.tsx'
import { NotFoundPage } from './pages/NotFound.tsx';
import { SubscribePage } from './pages/Subscribe.tsx';


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
