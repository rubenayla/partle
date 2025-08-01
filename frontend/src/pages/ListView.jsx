// frontend/src/pages/ListView.jsx
import { Link } from "react-router-dom";

/**
 * Simple list view to unblock the UI.
 * – Uses static mock data if no `items` prop is passed.
 */
export default function ListView({ items }) {
  if (!Array.isArray(items)) {
    return <p className="text-red-600 dark:text-red-400">ListView: items must be an array</p>;
  }

  return (
    <ul className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4 w-full">
      {items.map((item) => (
        <li key={item.id} className="border border-gray-200 dark:border-gray-700 rounded-xl p-4 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition">
          {item.image_url && (
            <img
              src={item.image_url}
              alt={item.name}
              className="w-full h-32 object-cover rounded mb-2"
            />
          )}
          <h3 className="font-semibold mb-1">
            {item.price ? (
              <Link to={`/products/${item.id}`} className="text-gray-900 dark:text-white hover:underline">
                {item.name}
              </Link>
            ) : (
              <Link to={`/stores/${item.id}`} className="text-gray-900 dark:text-white hover:underline">
                {item.name}
              </Link>
            )}
          </h3>
          {item.price ? (
            <p className="text-sm text-gray-600 dark:text-gray-300">€{item.price} — {item.store}</p>
          ) : (
            <p className="text-sm text-gray-600 dark:text-gray-300">{item.address || item.homepage || 'No additional info'}</p>
          )}
        </li>
      ))}
    </ul>
  );
}
