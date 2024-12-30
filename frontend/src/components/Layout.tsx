import React from 'react';
import type { ReactNode } from 'react';
import { useAuth } from 'react-oidc-context';
import { useNavigate } from 'react-router-dom';
import { appRoutes } from '../constants.ts';

type NavItemType = {
  text: string;
  /** Setting this flag to `true` means that only auth'd users should see the nav item */
  protected: boolean;
  action: () => void;
};

interface LayoutProps {
  children: ReactNode;
}

export const Layout: React.FC<LayoutProps> = (props) => {
    const { children } = props;
    const auth = useAuth();
    const navigate = useNavigate();
  
    const navItems: NavItemType[] = [
      {
        text: 'Home',
        protected: true,
        action: () => {
          navigate(appRoutes.home);
        }
      },
      {
        text: 'Logout',
        protected: false,
        action: () => {
          void auth.signoutRedirect();
        }
      },
      {
        text: "Birthing Person",
        protected: true,
        action: () => {
            navigate(appRoutes.birthingPerson);
        }
      }
    ].filter((item) => {
      return auth.isAuthenticated || !item.protected;
    });

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="fixed w-72 h-full bg-white border-r border-gray-200 p-6">
        {/* Brand */}
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 bg-pink-400 rounded-xl"></div>
          <span className="text-xl font-semibold text-gray-900">Labour Tracker</span>
        </div>

        {/* Navigation */}
        <nav>
          <div className="mb-6">
            <div className="text-xs font-medium text-gray-500 uppercase tracking-wider px-4 mb-3">
              Overview
            </div>
            <div className="flex flex-col gap-2">
                {
                navItems.map((item) => (
                    <a className="flex items-center gap-3 px-4 py-3 text-gray-600 hover:bg-pink-50 hover:text-pink-500 rounded-lg" key={item.text} onClick={item.action}>
                        {item.text}
                    </a>
                ))}
            </div>
          </div>
        </nav>
      </aside>

        <main className="ml-72 p-8">
            <header className="mb-8">
                <h1 className="text-3xl font-semibold text-gray-900 mb-2">Dashboard</h1>
                <p className="text-gray-500">Track your labor progress and manage your information.</p>
            </header>
            {children}
        </main>
    </div>
  );
};