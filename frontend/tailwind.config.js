/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Earth tone color palette
        earth: {
          50: '#faf8f5',
          100: '#f3f0e8',
          200: '#e6dfd1',
          300: '#d4c9b3',
          400: '#c0b195',
          500: '#a8957a',
          600: '#8f7a5f',
          700: '#75624c',
          800: '#5f4f3e',
          900: '#4d4033',
        },
        sage: {
          50: '#f6f7f4',
          100: '#e8ebe4',
          200: '#d1d7c8',
          300: '#b3c0a6',
          400: '#95a884',
          500: '#7a8f6b',
          600: '#5f7352',
          700: '#4d5c42',
          800: '#3f4a36',
          900: '#343d2e',
        },
        tan: {
          50: '#fdfcf9',
          100: '#faf7f0',
          200: '#f3ede0',
          300: '#e9e0c9',
          400: '#ddcfab',
          500: '#d0be8a',
          600: '#c1a86b',
          700: '#a68f56',
          800: '#8a7448',
          900: '#6f5d3a',
        },
        forest: {
          50: '#f0f4f0',
          100: '#dde6dd',
          200: '#bccdc0',
          300: '#94b09a',
          400: '#6d8f75',
          500: '#517259',
          600: '#3f5a47',
          700: '#34483a',
          800: '#2c3a30',
          900: '#253028',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
