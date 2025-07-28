// frontend/src/pages/ListView.jsx
import { Link } from "react-router-dom";

/**
 * Simple list view to unblock the UI.
 * – Uses static mock data if no `items` prop is passed.
 */
export default function ListView({ items }) {
  if (!Array.isArray(items)) {
    return <p className="text-danger">ListView: items must be an array</p>;
  }

  return (
    <ul className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4 w-full">
      {items.map((item) => (
        <li key={item.id} className="border border-surface-hover rounded-xl p-4 bg-surface hover:bg-surface-hover transition">
          {item.image_url && (
            <img
              src={item.image_url}
              alt={item.name}
              className="w-full h-32 object-cover rounded mb-2"
            />
          )}
          <h3 className="font-semibold mb-1">
            {item.price ? (
              <Link to={`/products/${item.id}`} className="text-foreground hover:underline">
                {item.name}
              </Link>
            ) : (
              <Link to={`/stores/${item.id}`} className="text-foreground hover:underline">
                {item.name}
              </Link>
            )}
          </h3>
          {item.price ? (
            <p className="text-sm text-muted">€{item.price} — {item.store}</p>
          ) : (
            <p className="text-sm text-muted">{item.address || item.homepage || 'No additional info'}</p>
          )}
        </li>
      ))}
    </ul>
  );
}
