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
        'text-secondary':  'var(--color-text-secondary)', // text-muted
        muted:             'var(--color-text-secondary)', // text-muted (alias)
        disabled:          'var(--color-text-disabled)',  // text-disabled

        /* Primary brand color palette */
        primary: {
          50:              'var(--color-primary-50)',
          100:             'var(--color-primary-100)',
          200:             'var(--color-primary-200)',
          300:             'var(--color-primary-300)',
          400:             'var(--color-primary-400)',
          DEFAULT:         'var(--color-primary)',        // #0b57d0
          500:             'var(--color-primary)',
          600:             'var(--color-primary-600)',
          700:             'var(--color-primary-700)',
          800:             'var(--color-primary-800)',
          900:             'var(--color-primary-900)',
        },

        /* Accent & actions */
        accent:            'var(--color-primary)',        // bg-accent, text-accent
        'accent-hover':    'var(--color-primary-hover)',

        /* Links */
        link:              'var(--color-link)',           // text-link
        'link-hover':      'var(--color-link-hover)',

        /* States */
        focus:             'var(--color-focus)',
        danger:            'var(--color-danger)',
        success:           'var(--color-success)',
        warning:           'var(--color-warning)',
      },
    },
  },
  plugins: [],
};
