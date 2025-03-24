import React, { lazy, Suspense } from 'react';
import { Navigate } from 'react-router-dom';
import Loader from './components/common/Loader';

// Lazy load components for better performance
const Home = lazy(() => import('./pages/Home'));
const BaseballIndex = lazy(() => import('./pages/Baseball'));
const GameDetails = lazy(() => import('./pages/Baseball/GameDetails'));
const NotFound = lazy(() => import('./pages/NotFound'));

// Loading fallback
const LoadingFallback = () => (
  <div className="flex items-center justify-center h-64">
    <Loader size="lg" />
  </div>
);

/**
 * Application routes configuration
 */
const routes = [
  {
    path: '/',
    element: (
      <Suspense fallback={<LoadingFallback />}>
        <Home />
      </Suspense>
    ),
    exact: true,
  },
  {
    path: '/baseball',
    element: (
      <Suspense fallback={<LoadingFallback />}>
        <BaseballIndex />
      </Suspense>
    ),
    exact: true,
  },
  {
    path: '/baseball/:gameId',
    element: (
      <Suspense fallback={<LoadingFallback />}>
        <GameDetails />
      </Suspense>
    ),
    exact: true,
  },
  {
    path: '/football',
    element: <Navigate to="/" replace />,
  },
  {
    path: '/basketball',
    element: <Navigate to="/" replace />,
  },
  {
    path: '*',
    element: (
      <Suspense fallback={<LoadingFallback />}>
        <NotFound />
      </Suspense>
    ),
  }
];

export default routes;