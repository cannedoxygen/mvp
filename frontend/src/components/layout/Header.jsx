import React from 'react';
import { Link, NavLink } from 'react-router-dom';

/**
 * Header component with navigation
 */
const Header = () => {
  return (
    <header className="bg-white shadow">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and site name */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <span className="text-xl font-bold text-primary-600">Baseball Betting Simulator</span>
            </Link>
          </div>
          
          {/* Main navigation */}
          <nav className="flex items-center">
            <ul className="flex space-x-4">
              <li>
                <NavLink 
                  to="/baseball" 
                  className={({ isActive }) => 
                    isActive 
                      ? "text-primary-600 font-medium" 
                      : "text-gray-600 hover:text-primary-600"
                  }
                >
                  Baseball
                </NavLink>
              </li>
              <li>
                <span className="text-gray-400 cursor-not-allowed">Football</span>
              </li>
              <li>
                <span className="text-gray-400 cursor-not-allowed">Basketball</span>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;