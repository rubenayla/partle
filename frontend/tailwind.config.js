// tailwind.config.js
module.exports = {
  darkMode: 'class', // Toggle dark mode via <html class="dark">
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        background:       'var(--color-background)',
        surface:          'var(--color-surface)',
        primary:          'var(--color-primary)',
        danger:           'var(--color-danger)',
        'text-primary':   'var(--color-text-primary)',
        'text-secondary': 'var(--color-text-secondary)',
      },
    },
  },
  plugins: [],
}
