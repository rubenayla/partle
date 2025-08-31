import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
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

// Mock the auth hook
vi.mock("../../hooks/useAuth.jsx", () => ({
  useAuth: vi.fn(),
  AuthProvider: ({ children }) => children,
}));

// Import the mocked hook
import { useAuth } from "../../hooks/useAuth.jsx";

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

const mockUser = {
  id: 123,
  email: "test@example.com"
};

const mockOtherUser = {
  id: 456,
  email: "other@example.com"
};

// Helper component to wrap ProductDetail with all necessary providers
const TestWrapper = ({ children }) => {
  return (
    <HelmetProvider>
      <MemoryRouter initialEntries={["/products/1"]}>
        <Routes>
          <Route path="/products/:id" element={children} />
        </Routes>
      </MemoryRouter>
    </HelmetProvider>
  );
};

describe("ProductDetail", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
    
    // Default successful API response
    api.get.mockImplementation((url) => {
      if (url === "/v1/products/1/") {
        return Promise.resolve({ data: mockProduct });
      }
      return Promise.reject(new Error("Not found"));
    });
    
    // Default auth state
    useAuth.mockReturnValue({
      user: null,
      signIn: vi.fn(),
      register: vi.fn(),
      isLoading: false
    });
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  describe("when not logged in", () => {
    it("shows product details without edit controls", async () => {
      useAuth.mockReturnValue({
        user: null,
        signIn: vi.fn(),
        register: vi.fn(),
        isLoading: false
      });

      render(
        <TestWrapper>
          <ProductDetail />
        </TestWrapper>
      );

      // Wait for product to load
      await waitFor(() => {
        expect(screen.getByText("Test Product")).toBeInTheDocument();
      });

      // Should show product details
      expect(screen.getByText("Test Product")).toBeInTheDocument();
      expect(screen.getByText("Test description")).toBeInTheDocument();
      expect(screen.getByText("Price: €29.99")).toBeInTheDocument();
      expect(screen.getByRole("link", { name: "https://example.com/product" })).toBeInTheDocument();

      // Should NOT show edit button
      expect(screen.queryByText("Edit")).not.toBeInTheDocument();
      expect(screen.queryByText("Save")).not.toBeInTheDocument();
      expect(screen.queryByText("Cancel")).not.toBeInTheDocument();
    });

    it("shows loading state initially", () => {
      render(
        <TestWrapper>
          <ProductDetail />
        </TestWrapper>
      );

      expect(screen.getByText("Loading…")).toBeInTheDocument();
    });
  });

  describe("when logged in but not the owner", () => {
    it("shows product details without edit controls", async () => {
      useAuth.mockReturnValue({
        user: mockOtherUser,
        signIn: vi.fn(),
        register: vi.fn(),
        isLoading: false
      });

      render(
        <TestWrapper>
          <ProductDetail />
        </TestWrapper>
      );

      // Wait for product to load
      await waitFor(() => {
        expect(screen.getByText("Test Product")).toBeInTheDocument();
      });

      // Should show product details
      expect(screen.getByText("Test Product")).toBeInTheDocument();
      expect(screen.getByText("Test description")).toBeInTheDocument();

      // Should NOT show edit button (different user)
      expect(screen.queryByText("Edit")).not.toBeInTheDocument();
    });
  });

  describe("when logged in as the owner", () => {
    it("shows edit button and allows editing", async () => {
      useAuth.mockReturnValue({
        user: mockUser,
        signIn: vi.fn(),
        register: vi.fn(),
        isLoading: false
      });

      render(
        <TestWrapper>
          <ProductDetail />
        </TestWrapper>
      );

      // Wait for product to load
      await waitFor(() => {
        expect(screen.getByText("Test Product")).toBeInTheDocument();
      });

      // Should show edit button (same user ID as creator_id)
      await waitFor(() => {
        expect(screen.getByText("Edit")).toBeInTheDocument();
      });

      // Click edit button
      fireEvent.click(screen.getByText("Edit"));

      // Should show editing form
      expect(screen.getByDisplayValue("Test Product")).toBeInTheDocument();
      expect(screen.getByDisplayValue("Test description")).toBeInTheDocument();
      expect(screen.getByDisplayValue("29.99")).toBeInTheDocument();
      expect(screen.getByDisplayValue("https://example.com/product")).toBeInTheDocument();
      expect(screen.getByDisplayValue("https://example.com/image.jpg")).toBeInTheDocument();

      // Should show Save and Cancel buttons
      expect(screen.getByText("Save")).toBeInTheDocument();
      expect(screen.getByText("Cancel")).toBeInTheDocument();

      // Edit button should be hidden
      expect(screen.queryByText("Edit")).not.toBeInTheDocument();
    });

    it("allows canceling edit mode", async () => {
      useAuth.mockReturnValue({
        user: mockUser,
        signIn: vi.fn(),
        register: vi.fn(),
        isLoading: false
      });

      render(
        <TestWrapper>
          <ProductDetail />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText("Test Product")).toBeInTheDocument();
      });

      // Enter edit mode
      fireEvent.click(screen.getByText("Edit"));
      expect(screen.getByDisplayValue("Test Product")).toBeInTheDocument();

      // Make a change
      const nameInput = screen.getByDisplayValue("Test Product");
      fireEvent.change(nameInput, { target: { value: "Modified Name" } });
      expect(screen.getByDisplayValue("Modified Name")).toBeInTheDocument();

      // Cancel editing
      fireEvent.click(screen.getByText("Cancel"));

      // Should return to view mode with original values
      expect(screen.getByText("Test Product")).toBeInTheDocument();
      expect(screen.getByText("Edit")).toBeInTheDocument();
      expect(screen.queryByText("Save")).not.toBeInTheDocument();
      expect(screen.queryByText("Cancel")).not.toBeInTheDocument();
    });

    it("saves changes when form is submitted", async () => {
      const updatedProduct = {
        ...mockProduct,
        name: "Updated Product",
        description: "Updated description",
        price: 39.99
      };

      api.patch.mockResolvedValueOnce({ data: updatedProduct });

      render(
        <TestWrapper user={mockUser}>
          <ProductDetail />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText("Test Product")).toBeInTheDocument();
      });

      // Enter edit mode
      fireEvent.click(screen.getByText("Edit"));

      // Make changes
      const nameInput = screen.getByDisplayValue("Test Product");
      const descriptionInput = screen.getByDisplayValue("Test description");
      const priceInput = screen.getByDisplayValue("29.99");

      fireEvent.change(nameInput, { target: { value: "Updated Product" } });
      fireEvent.change(descriptionInput, { target: { value: "Updated description" } });
      fireEvent.change(priceInput, { target: { value: "39.99" } });

      // Save changes
      fireEvent.click(screen.getByText("Save"));

      // Should call API with correct data
      await waitFor(() => {
        expect(api.patch).toHaveBeenCalledWith("/v1/products/1/", {
          name: "Updated Product",
          description: "Updated description",
          price: 39.99,
          url: "https://example.com/product",
          image_url: "https://example.com/image.jpg"
        });
      });

      // Should return to view mode with updated values
      await waitFor(() => {
        expect(screen.getByText("Updated Product")).toBeInTheDocument();
        expect(screen.getByText("Updated description")).toBeInTheDocument();
        expect(screen.getByText("Price: €39.99")).toBeInTheDocument();
        expect(screen.getByText("Edit")).toBeInTheDocument();
      });
    });

    it("shows saving state during API call", async () => {
      // Mock a delayed API response
      api.patch.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({ data: mockProduct }), 100))
      );

      render(
        <TestWrapper user={mockUser}>
          <ProductDetail />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText("Test Product")).toBeInTheDocument();
      });

      // Enter edit mode and save
      fireEvent.click(screen.getByText("Edit"));
      fireEvent.click(screen.getByText("Save"));

      // Should show saving state
      expect(screen.getByText("Saving...")).toBeInTheDocument();
      expect(screen.getByText("Saving...")).toBeDisabled();

      // Wait for save to complete
      await waitFor(() => {
        expect(screen.getByText("Edit")).toBeInTheDocument();
      });
    });

    it("disables save button when name is empty", async () => {
      render(
        <TestWrapper user={mockUser}>
          <ProductDetail />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText("Test Product")).toBeInTheDocument();
      });

      // Enter edit mode
      fireEvent.click(screen.getByText("Edit"));

      // Clear the name
      const nameInput = screen.getByDisplayValue("Test Product");
      fireEvent.change(nameInput, { target: { value: "" } });

      // Save button should be disabled
      const saveButton = screen.getByText("Save");
      expect(saveButton).toBeDisabled();
    });

    it("handles API errors during save", async () => {
      api.patch.mockRejectedValueOnce(new Error("Network error"));
      
      // Mock alert
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {});

      render(
        <TestWrapper user={mockUser}>
          <ProductDetail />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(screen.getByText("Test Product")).toBeInTheDocument();
      });

      // Enter edit mode and try to save
      fireEvent.click(screen.getByText("Edit"));
      fireEvent.click(screen.getByText("Save"));

      // Should show error message
      await waitFor(() => {
        expect(alertSpy).toHaveBeenCalledWith("Failed to update product. Please try again.");
      });

      // Should remain in edit mode
      expect(screen.queryByText("Edit")).not.toBeInTheDocument();
      expect(screen.getByText("Save")).toBeInTheDocument();

      alertSpy.mockRestore();
    });
  });

  describe("product loading", () => {
    it("handles product not found", async () => {
      api.get.mockRejectedValueOnce({ 
        response: { status: 404 } 
      });

      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

      render(
        <TestWrapper user={mockUser}>
          <ProductDetail />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(consoleSpy).toHaveBeenCalledWith("Product not found");
      });

      consoleSpy.mockRestore();
    });

    it("calls API with correct product ID from URL", async () => {
      render(
        <TestWrapper user={mockUser}>
          <ProductDetail />
        </TestWrapper>
      );

      await waitFor(() => {
        expect(api.get).toHaveBeenCalledWith("/v1/products/1/");
      });
    });
  });
});