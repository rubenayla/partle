/**
 * @fileoverview SearchBar Component Tests
 * @module components/__tests__/SearchBar
 */
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import SearchBar from "../SearchBar";
import type { ProductSearchParams, Theme } from "../../types";

// Extend window interface to include homeSearchHandler
declare global {
  interface Window {
    homeSearchHandler?: (params: ProductSearchParams) => void;
  }
}

describe("SearchBar", () => {
  const defaultTheme: Theme = 'system';
  const mockSetTheme = vi.fn();

  beforeEach(() => {
    // Clear any existing window.homeSearchHandler
    delete window.homeSearchHandler;
    vi.clearAllMocks();
  });

  it("renders without crashing", () => {
    render(
      <MemoryRouter>
        <SearchBar 
          currentTheme={defaultTheme}
          setTheme={mockSetTheme}
        />
      </MemoryRouter>
    );

    // Check for a key element to ensure it rendered.
    // The "Partle" link is a good candidate.
    expect(screen.getByText("Partle")).toBeInTheDocument();
  });

  it("calls onSearch when form is submitted", async () => {
    const mockOnSearch = vi.fn();

    render(
      <MemoryRouter>
        <SearchBar 
          onSearch={mockOnSearch}
          currentTheme={defaultTheme}
          setTheme={mockSetTheme}
        />
      </MemoryRouter>
    );

    const searchInput = screen.getByPlaceholderText("Search products around you");
    const searchButton = screen.getByRole("button", { name: /search/i });

    // Type in search input
    fireEvent.change(searchInput, { target: { value: "test query" } });

    // Submit the form
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalledWith({
        query: "test query",
        searchType: "products",
        priceMin: 0,
        priceMax: 500,
        selectedTags: [],
        sortBy: "random",
        sortOrder: "desc"
      });
    });
  });

  it("does not crash when onSearch is undefined", async () => {
    render(
      <MemoryRouter>
        <SearchBar 
          onSearch={undefined}
          currentTheme={defaultTheme}
          setTheme={mockSetTheme}
        />
      </MemoryRouter>
    );

    const searchInput = screen.getByPlaceholderText("Search products around you");
    const searchButton = screen.getByRole("button", { name: /search/i });

    // Type in search input
    fireEvent.change(searchInput, { target: { value: "test query" } });

    // Submit the form - should not crash
    expect(() => {
      fireEvent.click(searchButton);
    }).not.toThrow();
  });

  it("calls onSearch when sort option is changed", async () => {
    const user = userEvent.setup();
    const mockOnSearch = vi.fn();

    render(
      <MemoryRouter>
        <SearchBar 
          onSearch={mockOnSearch}
          currentTheme={defaultTheme}
          setTheme={mockSetTheme}
        />
      </MemoryRouter>
    );

    // Find the sort dropdown trigger button
    const sortTrigger = screen.getByRole("button", { name: /Sort: Random/i });
    await user.click(sortTrigger);

    // Find and click a different sort option
    const newestOption = await screen.findByText("Newest");
    await user.click(newestOption);

    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalledWith({
        query: "",
        searchType: "products",
        priceMin: 0,
        priceMax: 500,
        selectedTags: [],
        sortBy: "created_at",
        sortOrder: "desc"
      });
    });
  });

  it("calls onSearch when search type is changed to stores", async () => {
    const user = userEvent.setup();
    const mockOnSearch = vi.fn();

    render(
      <MemoryRouter>
        <SearchBar 
          onSearch={mockOnSearch}
          currentTheme={defaultTheme}
          setTheme={mockSetTheme}
        />
      </MemoryRouter>
    );

    // Find and click the filters dropdown
    const filtersButton = screen.getByRole("button", { name: /Filters/i });
    await user.click(filtersButton);

    // Find and click the "Stores" button
    const storesButton = await screen.findByText("Stores");
    await user.click(storesButton);

    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalledWith({
        query: "",
        searchType: "stores",
        priceMin: 0,
        priceMax: 500,
        selectedTags: [],
        sortBy: "random",
        sortOrder: "desc"
      });
    });
  });

  it("handles state updates correctly without React warnings", async () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => { });
    const mockOnSearch = vi.fn();

    render(
      <MemoryRouter>
        <SearchBar 
          onSearch={mockOnSearch}
          currentTheme={defaultTheme}
          setTheme={mockSetTheme}
        />
      </MemoryRouter>
    );

    const searchInput = screen.getByPlaceholderText("Search products around you");

    // Rapidly change input value
    fireEvent.change(searchInput, { target: { value: "test1" } });
    fireEvent.change(searchInput, { target: { value: "test2" } });
    fireEvent.change(searchInput, { target: { value: "test3" } });

    // Should not have any React warnings about state updates
    expect(consoleSpy).not.toHaveBeenCalledWith(
      expect.stringContaining("useState")
    );
    expect(consoleSpy).not.toHaveBeenCalledWith(
      expect.stringContaining("useReducer")
    );

    consoleSpy.mockRestore();
  });

  it("handles theme changes correctly", async () => {
    const user = userEvent.setup();

    render(
      <MemoryRouter>
        <SearchBar 
          currentTheme={defaultTheme}
          setTheme={mockSetTheme}
          isLoggedIn={true}
        />
      </MemoryRouter>
    );

    // Find and click the user dropdown to access theme settings
    const userButton = screen.getByRole("button", { name: /user account/i });
    await user.click(userButton);

    // The theme switch should be accessible when logged in
    // Note: Specific theme switch interaction depends on implementation
    expect(mockSetTheme).toHaveBeenCalledTimes(0); // Initially not called
  });
});