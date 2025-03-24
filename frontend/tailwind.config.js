/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./index.html",
      "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
      extend: {
        colors: {
          primary: {
            50: '#f0f9ff',
            100: '#e0f2fe',
            200: '#bae6fd',
            300: '#7dd3fc',
            400: '#38bdf8',
            500: '#0ea5e9',
            600: '#0284c7',
            700: '#0369a1',
            800: '#075985',
            900: '#0c4a6e',
            950: '#082f49',
          },
          betting: {
            positive: '#10b981', // emerald-500
            negative: '#ef4444', // red-500
            neutral: '#6b7280', // gray-500
            value: '#f59e0b', // amber-500
          },
          team: {
            home: '#3b82f6', // blue-500
            away: '#ec4899', // pink-500
          },
          surface: {
            card: '#ffffff',
            background: '#f9fafb',
            dark: '#1f2937',
          }
        },
        fontFamily: {
          sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
          mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
        },
      },
    },
    plugins: [],
  }