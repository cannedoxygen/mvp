import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ReactQueryDevtools } from 'react-query/devtools';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Layout components
import Layout from './components/layout/Layout';

// Page components
import Home from './pages/Home';
import BaseballIndex from './pages/Baseball';
import GameDetails from './pages/Baseball/GameDetails';
import NotFound from './pages/NotFound';

// Initialize React Query client with better defaults for API data
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: (failureCount, error) => {
        // Don't retry for 404 errors
        if (error?.response?.status === 404) return false;
        // Retry up to 2 times for other errors
        return failureCount < 2;
      },
      onError: (err) => {
        console.error('Query error:', err);
      }
    },
    mutations: {
      onError: (err) => {
        console.error('Mutation error:', err);
      }
    }
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            {/* Home page */}
            <Route index element={<Home />} />
            
            {/* Baseball routes */}
            <Route path="baseball">
              <Route index element={<BaseballIndex />} />
              <Route path=":gameId" element={<GameDetails />} />
            </Route>
            
            {/* Future expansion placeholders */}
            <Route path="football" element={<Navigate to="/" replace />} />
            <Route path="basketball" element={<Navigate to="/" replace />} />
            
            {/* 404 page */}
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </Router>
      
      {/* Toast notifications for API success/error messages */}
      <ToastContainer position="top-right" autoClose={5000} />
      
      {/* React Query Devtools - only in development */}
      {process.env.NODE_ENV === 'development' && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  );
}

export default App;