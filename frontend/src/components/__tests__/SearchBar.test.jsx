import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import SearchBar from "../SearchBar";

describe("SearchBar", () => {
  beforeEach(() => {
    // Clear any existing window.homeSearchHandler
    delete window.homeSearchHandler;
  });

  it("renders without crashing", () => {
    render(
      <MemoryRouter>
        <SearchBar />
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
        <SearchBar onSearch={mockOnSearch} />
      </MemoryRouter>
    );

    const searchInput = screen.getByPlaceholderText("What are you looking for?");
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
        sortBy: "random"
      });
    });
  });

  it("does not crash when onSearch is undefined", async () => {
    render(
      <MemoryRouter>
        <SearchBar onSearch={undefined} />
      </MemoryRouter>
    );

    const searchInput = screen.getByPlaceholderText("What are you looking for?");
    const searchButton = screen.getByRole("button", { name: /search/i });

    // Type in search input
    fireEvent.change(searchInput, { target: { value: "test query" } });
    
    // Submit the form - should not crash
    expect(() => {
      fireEvent.click(searchButton);
    }).not.toThrow();
  });

  it("does not crash when onSearch is null", async () => {
    render(
      <MemoryRouter>
        <SearchBar onSearch={null} />
      </MemoryRouter>
    );

    const searchInput = screen.getByPlaceholderText("What are you looking for?");
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
        <SearchBar onSearch={mockOnSearch} />
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
        sortBy: "created_at"
      });
    });
  });

  it("calls onSearch when search type is changed to stores", async () => {
    const user = userEvent.setup();
    const mockOnSearch = vi.fn();
    
    render(
      <MemoryRouter>
        <SearchBar onSearch={mockOnSearch} />
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
        sortBy: "random"
      });
    });
  });

  it("handles state updates correctly without React warnings", async () => {
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    const mockOnSearch = vi.fn();
    
    render(
      <MemoryRouter>
        <SearchBar onSearch={mockOnSearch} />
      </MemoryRouter>
    );

    const searchInput = screen.getByPlaceholderText("What are you looking for?");
    
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
});
