import { createContext, useContext, useEffect, useState, ReactNode } from 'react'

export type ThemeMode = 'light' | 'auto' | 'dark'

interface ThemeContextValue {
  theme: ThemeMode
  setTheme: (mode: ThemeMode) => void
}

const ThemeContext = createContext<ThemeContextValue>({
  theme: 'auto',
  setTheme: () => {}
})

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<ThemeMode>(() => {
    return (localStorage.getItem('theme') as ThemeMode) || 'auto'
  })

  useEffect(() => {
    const root = document.documentElement
    const apply = (mode: 'light' | 'dark') => {
      if (mode === 'dark') root.classList.add('dark')
      else root.classList.remove('dark')
    }

    let media: MediaQueryList
    if (theme === 'auto') {
      media = window.matchMedia('(prefers-color-scheme: dark)')
      apply(media.matches ? 'dark' : 'light')
      const handler = (e: MediaQueryListEvent) => apply(e.matches ? 'dark' : 'light')
      media.addEventListener('change', handler)
      return () => media.removeEventListener('change', handler)
    } else {
      apply(theme)
    }

    localStorage.setItem('theme', theme)
  }, [theme])

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  return useContext(ThemeContext)
}
