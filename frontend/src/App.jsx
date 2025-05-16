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
      <div className="bg-gray-100 p-4 rounded text-gray-600">
        👋 Tailwind is working.
      </div>
    </main>
  );
}
