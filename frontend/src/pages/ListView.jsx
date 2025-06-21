// frontend/src/pages/ListView.jsx
import { Link } from "react-router-dom";

/**
 * Simple list view to unblock the UI.
 * – Uses static mock data if no `products` prop is passed.
 */
export default function ListView({ products }) {
  const items = products ?? [
    { id: 1, name: "M8 Left‑Hand Lock Nut", price: 1.2, store: "Ferretería Paco" },
    { id: 2, name: "JST‑XH 6‑pin", price: 0.5, store: "Electrónica Vega" },
  ];

  if (!Array.isArray(items)) {
    return <p className="text-danger">ListView: products must be an array</p>;
  }

  return (
    <ul className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
      {items.map((p) => (
        <li key={p.id} className="border border-surface-hover rounded-xl p-4 bg-surface hover:bg-surface-hover transition">
          <h3 className="font-semibold mb-1">
            <Link to={`/products/${p.id}`} className="text-foreground hover:underline">
              {p.name}
            </Link>
          </h3>
          <p className="text-sm text-muted">€{p.price} — {p.store}</p>
        </li>
      ))}
    </ul>
  );
}
