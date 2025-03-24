import React from 'react';
import ReactDOM from 'react-dom/client';
import { ErrorBoundary } from 'react-error-boundary';
import App from './App';
import './styles/tailwind.css';
import './styles/global.css';

// Error fallback component
const ErrorFallback = ({ error, resetErrorBoundary }) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-red-50">
      <div className="max-w-md text-center">
        <h1 className="text-xl font-bold text-red-600 mb-4">
          Something went wrong
        </h1>
        <div className="text-red-700 mb-4">
          {error.message || 'An unexpected error occurred'}
        </div>
        <button
          onClick={resetErrorBoundary}
          className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700"
        >
          Try again
        </button>
      </div>
    </div>
  );
};

// Root element
const rootElement = document.getElementById('root');

// Create root and render app
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  
  root.render(
    <React.StrictMode>
      <ErrorBoundary 
        FallbackComponent={ErrorFallback}
        onReset={() => {
          // Reset the app state here if needed
          window.location.href = '/';
        }}
      >
        <App />
      </ErrorBoundary>
    </React.StrictMode>
  );
} else {
  console.error('Root element not found');
}