export default function ListView({ results }) {
    return (
      <div className="flex flex-col gap-4">
        {results.map((item) => (
          <div key={item.storeId} className="border p-4 rounded shadow-sm">
            <div className="font-semibold text-lg">{item.name}</div>
            <div className="text-sm text-gray-600 mb-1">{item.storeName}</div>
            <div className="text-sm mb-2">
              €{item.price.toFixed(2)} • {item.qty} in stock • {item.distanceKm} km
            </div>
            <div className="flex gap-2">
              <a href={`tel:+34900000000`} className="text-blue-600 underline text-sm">
                📞 Call
              </a>
              <a
                href={`https://maps.google.com/?q=${item.lat},${item.lng}`}
                className="text-blue-600 underline text-sm"
                target="_blank"
                rel="noopener noreferrer"
              >
                📍 Navigate
              </a>
            </div>
          </div>
        ))}
      </div>
    );
  }
  