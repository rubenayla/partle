import { render, screen } from '@testing-library/react'
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import App from './App'

describe('App', () => {
  beforeEach(() => {
    global.fetch = vi.fn().mockResolvedValue({ ok: true }) as any
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the Home page by default', async () => {
    render(<App />)
    expect(await screen.findByText(/Latest products/i)).toBeInTheDocument()
  })
})
