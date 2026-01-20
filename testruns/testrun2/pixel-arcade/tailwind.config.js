/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cyberpunk-purple': '#8b5cf6',
        'cyberpunk-blue': '#3b82f6',
        'cyberpunk-green': '#10b981',
        'cyberpunk-dark': '#1e293b',
        'cyberpunk-darker': '#0f172a',
      },
      fontFamily: {
        'pixel': ['"Press Start 2P"', 'cursive'],
        'retro': ['"Silkscreen"', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}