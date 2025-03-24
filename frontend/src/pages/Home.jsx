import React from 'react';
import { Link } from 'react-router-dom';

/**
 * Home page / Landing page component
 * Displays sport selection options
 */
const Home = () => {
  return (
    <div className="py-8">
      {/* Page heading */}
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          AI-Enhanced Sports Betting Simulator
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Get data-driven predictions and betting insights powered by AI analysis and Monte Carlo simulations.
        </p>
      </div>

      {/* Sport selection cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
        {/* Baseball Card - Active */}
        <Link 
          to="/baseball" 
          className="bg-white shadow-md rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
        >
          <div className="p-6 text-center">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Baseball</h2>
            <p className="text-gray-600 mb-4">MLB game predictions and betting insights</p>
            <span className="inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
              Available Now
            </span>
          </div>
        </Link>

        {/* Football Card - Coming Soon */}
        <div className="bg-white shadow-md rounded-lg overflow-hidden opacity-70">
          <div className="p-6 text-center">
            <h2 className="text-xl font-semibold text-gray-700 mb-2">Football</h2>
            <p className="text-gray-500 mb-4">NFL game predictions and betting insights</p>
            <span className="inline-block bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm font-medium">
              Coming Soon
            </span>
          </div>
        </div>

        {/* Basketball Card - Coming Soon */}
        <div className="bg-white shadow-md rounded-lg overflow-hidden opacity-70">
          <div className="p-6 text-center">
            <h2 className="text-xl font-semibold text-gray-700 mb-2">Basketball</h2>
            <p className="text-gray-500 mb-4">NBA game predictions and betting insights</p>
            <span className="inline-block bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm font-medium">
              Coming Soon
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;