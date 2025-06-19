// frontend/src/pages/Home.jsx
import TopBar from "../components/TopBar";
import ListView from "./ListView";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-900">
      <TopBar />
      <main className="flex-1 p-4 w-full">
        <h2 className="text-lg font-semibold mb-4">Latest products</h2>
        <ListView />
      </main>
    </div>
  );
}
