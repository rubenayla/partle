import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App', () => {
  it('renders the Home page by default', () => {
    render(<App />);
    expect(screen.getByText(/Latest products/i)).toBeInTheDocument();
  });
});
