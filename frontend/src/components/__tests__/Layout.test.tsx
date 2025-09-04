import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import Layout from '../Layout';

// Simple mocks
vi.mock('../SearchBar', () => ({
  default: () => <div data-testid="search-bar">SearchBar</div>,
}));

vi.mock('../AuthModal', () => ({
  default: () => <div data-testid="auth-modal">AuthModal</div>,
}));

Object.defineProperty(window, 'localStorage', {
  value: { getItem: vi.fn(() => null) },
});

describe('Layout', () => {
  it('renders correctly', () => {
    render(
      <MemoryRouter>
        <Layout setTheme={vi.fn()} currentTheme="light">
          <div data-testid="content">Test</div>
        </Layout>
      </MemoryRouter>
    );
    
    expect(screen.getByTestId('search-bar')).toBeInTheDocument();
    expect(screen.getByTestId('content')).toBeInTheDocument();
  });
});