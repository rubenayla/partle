// frontend/src/pages/ListView.jsx

/**
 * Simple list view to unblock the UI.
 * – Uses static mock data if no `products` prop is passed.
 */
export default function ListView({ products }) {
  const items = products ?? [
    { id: 1, name: "M8 Left‑Hand Lock Nut", price: 1.2, store: "Ferretería Paco" },
    { id: 2, name: "JST‑XH 6‑pin", price: 0.5, store: "Electrónica Vega" },
  ];

  if (!Array.isArray(items)) return <p className="text-red-600">ListView: products must be an array</p>;

  return (
    <ul className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
      {items.map((p) => (
        <li key={p.id} className="border rounded p-4 shadow-sm">
          <h3 className="font-semibold mb-1">{p.name}</h3>
          <p className="text-sm text-gray-600">€{p.price} — {p.store}</p>
        </li>
      ))}
    </ul>
  );
}
