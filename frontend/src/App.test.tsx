import { render, screen } from '@testing-library/react'
import { describe, it, expect, afterEach, vi } from 'vitest'
import App from './App'

vi.mock('axios'); // Mock the axios module

describe('App', () => {
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('renders the Home page by default', async () => {
    render(<App />)
    expect(await screen.findByText(/Latest products/i)).toBeInTheDocument()
  })
})
