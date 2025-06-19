// frontend/src/pages/Home.jsx
import SearchBar from "../components/SearchBar";
import ListView from "./ListView";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-white text-gray-900">
      <SearchBar />
      <main className="flex-1 p-4 w-full">
        <h2 className="text-lg font-semibold mb-4">Latest products</h2>
        <ListView />
      </main>
    </div>
  );
}
