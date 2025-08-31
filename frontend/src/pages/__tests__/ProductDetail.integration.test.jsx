import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import { HelmetProvider } from "react-helmet-async";
import ProductDetail from "../ProductDetail";
import api from "../../api/index.ts";

// Mock the API
vi.mock("../../api/index.ts", () => ({
  default: {
    get: vi.fn(),
    patch: vi.fn(),
  },
}));

// Mock the auth hook with a simple implementation
const mockUseAuth = vi.fn();
vi.mock("../../hooks/useAuth.jsx", () => ({
  useAuth: () => mockUseAuth(),
  AuthProvider: ({ children }) => children,
}));

// Test data
const mockProduct = {
  id: 1,
  name: "Test Product",
  description: "Test description",
  price: 29.99,
  url: "https://example.com/product",
  image_url: "https://example.com/image.jpg",
  creator_id: 123,
  store_id: null,
  created_at: "2024-01-01T00:00:00Z",
  updated_at: "2024-01-01T00:00:00Z",
  tags: []
};

const TestWrapper = ({ children }) => (
  <HelmetProvider>
    <MemoryRouter initialEntries={["/products/1"]}>
      <Routes>
        <Route path="/products/:id" element={children} />
      </Routes>
    </MemoryRouter>
  </HelmetProvider>
);

describe("ProductDetail Integration Tests", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    
    // Default API setup
    api.get.mockImplementation((url) => {
      if (url === "/v1/products/1/") {
        return Promise.resolve({ data: mockProduct });
      }
      return Promise.reject(new Error("Not found"));
    });
  });

  it("shows product without edit controls when not logged in", async () => {
    mockUseAuth.mockReturnValue({
      user: null,
      isLoading: false,
      signIn: vi.fn(),
      register: vi.fn()
    });

    render(
      <TestWrapper>
        <ProductDetail />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText("Test Product")).toBeInTheDocument();
    });

    // Product details should be visible
    expect(screen.getByText("Test description")).toBeInTheDocument();
    expect(screen.getByText("Price: €29.99")).toBeInTheDocument();

    // Edit controls should NOT be visible
    expect(screen.queryByText("Edit")).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /edit/i })).not.toBeInTheDocument();
  });

  it("shows product without edit controls when logged in as different user", async () => {
    mockUseAuth.mockReturnValue({
      user: { id: 999, email: "other@example.com" }, // Different user ID
      isLoading: false,
      signIn: vi.fn(),
      register: vi.fn()
    });

    render(
      <TestWrapper>
        <ProductDetail />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText("Test Product")).toBeInTheDocument();
    });

    // Product details should be visible
    expect(screen.getByText("Test description")).toBeInTheDocument();

    // Edit controls should NOT be visible (different user)
    expect(screen.queryByText("Edit")).not.toBeInTheDocument();
  });

  it("shows edit controls when logged in as product owner", async () => {
    mockUseAuth.mockReturnValue({
      user: { id: 123, email: "owner@example.com" }, // Same ID as product.creator_id
      isLoading: false,
      signIn: vi.fn(),
      register: vi.fn()
    });

    render(
      <TestWrapper>
        <ProductDetail />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText("Test Product")).toBeInTheDocument();
    });

    // Should show edit button for owner
    expect(screen.getByText("Edit")).toBeInTheDocument();
  });

  it("allows owner to edit and save product", async () => {
    const updatedProduct = {
      ...mockProduct,
      name: "Updated Product",
      description: "Updated description"
    };

    api.patch.mockResolvedValueOnce({ data: updatedProduct });

    mockUseAuth.mockReturnValue({
      user: { id: 123, email: "owner@example.com" },
      isLoading: false,
      signIn: vi.fn(),
      register: vi.fn()
    });

    render(
      <TestWrapper>
        <ProductDetail />
      </TestWrapper>
    );

    // Wait for product to load and edit button to appear
    await waitFor(() => {
      expect(screen.getByText("Edit")).toBeInTheDocument();
    });

    // Click edit
    fireEvent.click(screen.getByText("Edit"));

    // Should show editing form
    expect(screen.getByDisplayValue("Test Product")).toBeInTheDocument();
    expect(screen.getByDisplayValue("Test description")).toBeInTheDocument();

    // Make changes
    const nameInput = screen.getByDisplayValue("Test Product");
    const descInput = screen.getByDisplayValue("Test description");
    
    fireEvent.change(nameInput, { target: { value: "Updated Product" } });
    fireEvent.change(descInput, { target: { value: "Updated description" } });

    // Save changes
    fireEvent.click(screen.getByText("Save"));

    // Should call API with correct data
    await waitFor(() => {
      expect(api.patch).toHaveBeenCalledWith("/v1/products/1/", {
        name: "Updated Product",
        description: "Updated description",
        price: 29.99,
        url: "https://example.com/product",
        image_url: "https://example.com/image.jpg"
      });
    });

    // Should return to view mode
    await waitFor(() => {
      expect(screen.getByText("Updated Product")).toBeInTheDocument();
      expect(screen.getByText("Updated description")).toBeInTheDocument();
      expect(screen.getByText("Edit")).toBeInTheDocument();
    });
  });

  it("allows owner to cancel editing", async () => {
    mockUseAuth.mockReturnValue({
      user: { id: 123, email: "owner@example.com" },
      isLoading: false,
      signIn: vi.fn(),
      register: vi.fn()
    });

    render(
      <TestWrapper>
        <ProductDetail />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText("Edit")).toBeInTheDocument();
    });

    // Enter edit mode
    fireEvent.click(screen.getByText("Edit"));

    // Make changes
    const nameInput = screen.getByDisplayValue("Test Product");
    fireEvent.change(nameInput, { target: { value: "Changed Name" } });
    expect(screen.getByDisplayValue("Changed Name")).toBeInTheDocument();

    // Cancel
    fireEvent.click(screen.getByText("Cancel"));

    // Should return to original values
    expect(screen.getByText("Test Product")).toBeInTheDocument();
    expect(screen.getByText("Edit")).toBeInTheDocument();
    expect(screen.queryByText("Save")).not.toBeInTheDocument();
  });
});