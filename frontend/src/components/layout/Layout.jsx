import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';

/**
 * Main layout component that wraps all pages
 * Provides consistent header and footer across the application
 */
const Layout = () => {
  return (
    <div className="flex flex-col min-h-screen bg-surface-background">
      {/* Header */}
      <Header />
      
      {/* Main content */}
      <main className="flex-grow container mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <Outlet />
      </main>
      
      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Layout;