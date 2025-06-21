// tailwind.config.js
module.exports = {
  darkMode: 'class',          // html.dark enables dark palette
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx,css}',
  ],
  theme: {
    extend: {
      colors: {
        /* Layers */
        background:        'var(--color-background)',
        surface:           'var(--color-surface)',
        'surface-hover':   'var(--color-surface-hover)',

        /* Text */
        foreground:        'var(--color-text-primary)',   // text-foreground
        muted:             'var(--color-text-secondary)', // text-muted
        disabled:          'var(--color-text-disabled)',  // text-disabled

        /* Accent & actions */
        accent:            'var(--color-primary)',        // bg-accent, text-accent
        'accent-hover':    'var(--color-primary-hover)',

        /* Links */
        link:              'var(--color-link)',           // text-link
        'link-hover':      'var(--color-link-hover)',

        /* Other */
        focus:             'var(--color-focus)',
        danger:            'var(--color-danger)',
      },
    },
  },
  plugins: [],
};
