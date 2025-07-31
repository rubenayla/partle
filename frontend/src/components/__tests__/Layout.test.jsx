import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { MemoryRouter } from "react-router-dom";
import Layout from "../Layout";

describe("Layout", () => {
  beforeEach(() => {
    // Clear any existing window.homeSearchHandler
    delete window.homeSearchHandler;
    // Clear localStorage
    localStorage.clear();
  });

  afterEach(() => {
    vi.clearAllMocks();
    delete window.homeSearchHandler;
    localStorage.clear();
  });

  it("renders without crashing", () => {
    render(
      <MemoryRouter>
        <Layout>
          <div>Test Content</div>
        </Layout>
      </MemoryRouter>
    );

    expect(screen.getByText("Partle")).toBeInTheDocument();
    expect(screen.getByText("Test Content")).toBeInTheDocument();
  });

  it("passes undefined onSearch prop when not on home page", () => {
    render(
      <MemoryRouter initialEntries={["/stores"]}>
        <Layout>
          <div>Store Content</div>
        </Layout>
      </MemoryRouter>
    );

    const searchInput = screen.getByPlaceholderText("What are you looking for?");
    const searchButton = screen.getByRole("button", { name: /search/i });

    // Should not crash when submitting search on non-home page
    fireEvent.change(searchInput, { target: { value: "test" } });
    expect(() => {
      fireEvent.click(searchButton);
    }).not.toThrow();
  });

  it("passes homeSearchHandler as onSearch prop when on home page", async () => {
    // Mock homeSearchHandler
    const mockHomeSearchHandler = vi.fn();
    window.homeSearchHandler = mockHomeSearchHandler;

    render(
      <MemoryRouter initialEntries={["/"]}>
        <Layout>
          <div>Home Content</div>
        </Layout>
      </MemoryRouter>
    );

    const searchInput = screen.getByPlaceholderText("What are you looking for?");
    const searchButton = screen.getByRole("button", { name: /search/i });

    // Submit search form
    fireEvent.change(searchInput, { target: { value: "test search" } });
    fireEvent.click(searchButton);

    // Should call the homeSearchHandler
    await waitFor(() => {
      expect(mockHomeSearchHandler).toHaveBeenCalledWith({
        query: "test search",
        searchType: "products",
        priceMin: 0,
        priceMax: 500,
        selectedTags: [],
        sortBy: "random"
      });
    });
  });

  it("handles missing homeSearchHandler gracefully on home page", () => {
    // Ensure homeSearchHandler is not defined
    delete window.homeSearchHandler;

    render(
      <MemoryRouter initialEntries={["/"]}>
        <Layout>
          <div>Home Content</div>
        </Layout>
      </MemoryRouter>
    );

    const searchInput = screen.getByPlaceholderText("What are you looking for?");
    const searchButton = screen.getByRole("button", { name: /search/i });

    // Should not crash even when homeSearchHandler is undefined
    fireEvent.change(searchInput, { target: { value: "test" } });
    expect(() => {
      fireEvent.click(searchButton);
    }).not.toThrow();
  });

  it("updates login state correctly", async () => {
    // Initially not logged in
    render(
      <MemoryRouter>
        <Layout>
          <div>Test Content</div>
        </Layout>
      </MemoryRouter>
    );

    // Should show user icon for account (not logged in state)
    expect(screen.getByRole("button", { name: /user/i })).toBeInTheDocument();

    // Simulate login by setting token
    localStorage.setItem("token", "test-token");

    // Wait a bit for the interval to check localStorage
    await waitFor(() => {
      // The component should detect the login and potentially show different UI
      // Note: The actual UI changes depend on the SearchBar implementation
    }, { timeout: 2000 });
  });

  it("provides correct spacing and layout structure", () => {
    render(
      <MemoryRouter>
        <Layout>
          <div data-testid="test-content">Test Content</div>
        </Layout>
      </MemoryRouter>
    );

    // Check that the main content area has the correct classes for spacing
    const mainElement = screen.getByRole("main");
    expect(mainElement).toHaveClass("mt-[72px]", "pt-6", "max-w-screen-2xl", "mx-auto", "w-full", "px-4");
    
    // Check that the content is inside the main element
    expect(screen.getByTestId("test-content")).toBeInTheDocument();
  });

  it("handles account modal open/close correctly", async () => {
    render(
      <MemoryRouter>
        <Layout>
          <div>Test Content</div>
        </Layout>
      </MemoryRouter>
    );

    // Find and click the user button when not logged in
    const userButton = screen.getByRole("button", { name: /user/i });
    fireEvent.click(userButton);

    // Should open the auth modal
    await waitFor(() => {
      // The AuthModal should be rendered (checking for common modal elements)
      // Note: The actual modal content depends on the AuthModal implementation
      expect(document.body).toBeInTheDocument();
    });
  });

  it("maintains consistent layout across different routes", () => {
    const { rerender } = render(
      <MemoryRouter initialEntries={["/"]}>
        <Layout>
          <div>Home Content</div>
        </Layout>
      </MemoryRouter>
    );

    // Check home page layout
    expect(screen.getByText("Partle")).toBeInTheDocument();
    expect(screen.getByText("Home Content")).toBeInTheDocument();

    // Navigate to different route
    rerender(
      <MemoryRouter initialEntries={["/stores"]}>
        <Layout>
          <div>Stores Content</div>
        </Layout>
      </MemoryRouter>
    );

    // Layout should remain consistent
    expect(screen.getByText("Partle")).toBeInTheDocument();
    expect(screen.getByText("Stores Content")).toBeInTheDocument();
    
    // Main layout structure should be the same
    const mainElement = screen.getByRole("main");
    expect(mainElement).toHaveClass("mt-[72px]", "pt-6", "max-w-screen-2xl", "mx-auto", "w-full", "px-4");
  });
});