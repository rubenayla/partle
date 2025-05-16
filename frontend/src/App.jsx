import ListView from "./pages/ListView";

export default function App() {
  return (
    <main className="max-w-xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-blue-600 mb-4">
        Partle
      </h1>
      <input
        type="text"
        placeholder="Search a part (e.g. JST 6-pin)"
        className="w-full border rounded p-2 mb-4"
      />
      <ListView />
    </main>
  );
}
