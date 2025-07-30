import { render, screen, waitFor, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import Home from "../Home";

// Mock the api module
vi.mock("../../api", () => ({
  default: {
    get: vi.fn()
  }
}));

import api from "../../api";
const mockedApi = api;

// Mock the useInfiniteScroll hook
vi.mock("../../hooks/useInfiniteScroll", () => ({
  useInfiniteScroll: vi.fn(() => [false]) // Return [isFetching = false]
}));

describe("Home", () => {
  beforeEach(() => {
    // Clear any existing window.homeSearchHandler
    delete window.homeSearchHandler;
    
    // Mock api.get to return empty arrays by default
    mockedApi.get.mockResolvedValue({ data: [] });
  });

  afterEach(() => {
    vi.clearAllMocks();
    delete window.homeSearchHandler;
  });

  it("renders without crashing", async () => {
    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>
    );
    
    // Wait for initial render
    await waitFor(() => {
      expect(screen.getByText("Latest products")).toBeInTheDocument();
    });
  });

  it("sets up window.homeSearchHandler correctly", async () => {
    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>
    );
    
    // Wait for useEffect to run
    await waitFor(() => {
      expect(window.homeSearchHandler).toBeDefined();
      expect(typeof window.homeSearchHandler).toBe("function");
    });
  });

  it("homeSearchHandler updates search parameters correctly", async () => {
    // Mock axios to return sample data
    const mockProducts = [
      { id: 1, name: "Test Product", price: 10 }
    ];
    mockedApi.get.mockResolvedValue({ data: mockProducts });

    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>
    );
    
    // Wait for homeSearchHandler to be set up
    await waitFor(() => {
      expect(window.homeSearchHandler).toBeDefined();
    });

    // Call the search handler with new parameters
    const searchParams = {
      query: "test search",
      searchType: "products",
      priceMin: 10,
      priceMax: 100,
      selectedTags: ["tag1"],
      sortBy: "price_asc"
    };

    // This should not throw any React warnings
    await act(async () => {
      window.homeSearchHandler(searchParams);
    });

    // Wait for the API call to be made with correct parameters
    await waitFor(() => {
      expect(mockedApi.get).toHaveBeenCalledWith("/v1/products/", {
        params: {
          q: "test search",
          min_price: 10,
          max_price: 100,
          sort_by: "price_asc",
          tags: "tag1",
          limit: 20,
          offset: 0,
        },
      });
    });
  });

  it("homeSearchHandler handles stores search type", async () => {
    // Mock axios to return sample stores data
    const mockStores = [
      { id: 1, name: "Test Store", location: "Test Location" }
    ];
    mockedApi.get.mockResolvedValue({ data: mockStores });

    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>
    );
    
    // Wait for homeSearchHandler to be set up
    await waitFor(() => {
      expect(window.homeSearchHandler).toBeDefined();
    });

    // Call the search handler with stores search type
    const searchParams = {
      query: "store search",
      searchType: "stores",
      priceMin: 0,
      priceMax: 500,
      selectedTags: ["tag2"],
      sortBy: "relevance"
    };

    await act(async () => {
      window.homeSearchHandler(searchParams);
    });

    // Wait for the API call to be made to stores endpoint
    await waitFor(() => {
      expect(mockedApi.get).toHaveBeenCalledWith("/v1/stores/", {
        params: {
          q: "store search",
          sort_by: "relevance",
          tags: "tag2",
          limit: 20,
          offset: 0,
        },
      });
    });
  });

  it("does not cause React state update warnings", async () => {
    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
    
    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>
    );
    
    // Wait for homeSearchHandler to be set up
    await waitFor(() => {
      expect(window.homeSearchHandler).toBeDefined();
    });

    // Rapidly call the search handler multiple times
    const searchParams = {
      query: "rapid search",
      searchType: "products",
      priceMin: 0,
      priceMax: 500,
      selectedTags: [],
      sortBy: "relevance"
    };

    await act(async () => {
      window.homeSearchHandler(searchParams);
      window.homeSearchHandler({ ...searchParams, query: "rapid search 2" });
      window.homeSearchHandler({ ...searchParams, query: "rapid search 3" });
    });

    // Should not have any React warnings about state updates
    expect(consoleSpy).not.toHaveBeenCalledWith(
      expect.stringContaining("useState")
    );
    expect(consoleSpy).not.toHaveBeenCalledWith(
      expect.stringContaining("useReducer")
    );
    expect(consoleSpy).not.toHaveBeenCalledWith(
      expect.stringContaining("function")
    );
    
    consoleSpy.mockRestore();
  });

  it("cleans up homeSearchHandler on unmount", async () => {
    const { unmount } = render(<Home />);
    
    // Wait for homeSearchHandler to be set up
    await waitFor(() => {
      expect(window.homeSearchHandler).toBeDefined();
    });

    // Unmount the component
    unmount();

    // homeSearchHandler should be cleaned up
    expect(window.homeSearchHandler).toBeUndefined();
  });

  it("handles API errors gracefully", async () => {
    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
    
    // Mock api to throw an error
    mockedApi.get.mockRejectedValue(new Error("API Error"));

    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>
    );
    
    // Wait for homeSearchHandler to be set up
    await waitFor(() => {
      expect(window.homeSearchHandler).toBeDefined();
    });

    // Call the search handler - should not crash
    await act(async () => {
      window.homeSearchHandler({
        query: "error test",
        searchType: "products",
        priceMin: 0,
        priceMax: 500,
        selectedTags: [],
        sortBy: "relevance"
      });
    });

    // Should log the error but not crash
    await waitFor(() => {
      expect(consoleSpy).toHaveBeenCalledWith(
        "Error fetching products:",
        expect.any(Error)
      );
    });
    
    consoleSpy.mockRestore();
  });
});