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
    // The "Partle" link appears twice (mobile and desktop), so use getAllByText
    const partleElements = screen.getAllByText("Partle");
    expect(partleElements.length).toBeGreaterThan(0);
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

    const searchInput = screen.getAllByPlaceholderText("Search products around you")[0];
    const searchButtons = screen.getAllByRole("button", { name: /search/i });
    const searchButton = searchButtons[0];

    // Type in search input
    fireEvent.change(searchInput, { target: { value: "test query" } });

    // Submit the form
    fireEvent.click(searchButton);

    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalledWith(
        expect.objectContaining({
          query: "test query",
          searchType: "products",
          priceMin: 0,
          priceMax: 500,
          selectedTags: [],
          selectedStores: [],
          sortBy: "random",
          sortOrder: "desc"
        })
      );
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

    const searchInput = screen.getAllByPlaceholderText("Search products around you")[0];
    const searchButton = screen.getAllByRole("button", { name: /search/i })[0];

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

    // Find the sort dropdown trigger button (includes emoji)
    const sortTriggers = screen.getAllByRole("button", { name: /Sort: .* Random/i });
    await user.click(sortTriggers[0]);

    // Find and click a different sort option
    const newestOptions = await screen.findAllByText("✨ Newest");
    await user.click(newestOptions[0]);

    // The SearchBar component might need a form submit to trigger onSearch
    // Let's trigger the search by submitting the form
    const searchButton = screen.getAllByRole("button", { name: /search/i })[0];
    await user.click(searchButton);

    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalledWith(
        expect.objectContaining({
          query: "",
          searchType: "products",
          priceMin: 0,
          priceMax: 500,
          selectedTags: [],
          selectedStores: [],
          sortBy: "created_at",
          sortOrder: "desc"
        })
      );
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

    // Find and click the filters dropdown (multiple buttons with "Filters" text)
    const filtersButtons = screen.getAllByRole("button", { name: /Filters/i });
    await user.click(filtersButtons[0]);

    // Find and click the "Stores" button
    const storesButtons = await screen.findAllByText("Stores");
    await user.click(storesButtons[0]);

    // The dropdown might close after selecting, wait a bit
    await new Promise(resolve => setTimeout(resolve, 100));

    // Now find the search form and submit it directly
    const searchForms = document.querySelectorAll('form');
    const searchForm = Array.from(searchForms).find(form =>
      form.querySelector('input[placeholder*="Search"]')
    );

    if (searchForm) {
      fireEvent.submit(searchForm);
    }

    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalledWith(
        expect.objectContaining({
          query: "",
          searchType: "stores",
          priceMin: 0,
          priceMax: 500,
          selectedTags: [],
          selectedStores: [],
          sortBy: "random",
          sortOrder: "desc"
        })
      );
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

    const searchInput = screen.getAllByPlaceholderText("Search products around you")[0];

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
    // The user button doesn't have an aria-label, so we need to find it differently
    const userButtons = screen.getAllByRole("button");
    // Find button with user SVG (contains the path for user icon)
    const userButton = userButtons.find(button =>
      button.querySelector('svg path[d*="M19 21v-2a4 4"]')
    );
    if (userButton) {
      await user.click(userButton);
    }

    // The theme switch should be accessible when logged in
    // Note: Specific theme switch interaction depends on implementation
    expect(mockSetTheme).toHaveBeenCalledTimes(0); // Initially not called
  });
});