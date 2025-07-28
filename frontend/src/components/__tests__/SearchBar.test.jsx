import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { MemoryRouter } from "react-router-dom";
import SearchBar from "../SearchBar";

describe("SearchBar", () => {
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
});
