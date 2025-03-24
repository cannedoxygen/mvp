import React from 'react';

/**
 * Footer component with minimal information
 */
const Footer = () => {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="bg-gray-800 text-gray-300">
      <div className="container mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center">
          {/* Copyright */}
          <div className="mb-4 md:mb-0">
            <p className="text-sm">
              © {currentYear} Baseball Betting Simulator. For entertainment purposes only.
            </p>
          </div>
          
          {/* Disclaimer */}
          <div className="text-xs text-gray-400">
            <p>Simulated predictions. Not gambling advice.</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;