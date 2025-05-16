export default function MapView({ results }) {
    const center = [40.4168, -3.7038]; // Madrid
  
    return (
      <MapContainer center={center} zoom={12} className="h-[400px] w-full rounded">
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {results.map((item) => (
          <Marker key={item.storeId} position={[item.lat, item.lng]}>
            <Popup>
              <strong>{item.storeName}</strong><br />
              {item.partName}<br />
              €{item.price.toFixed(2)} • {item.qty} in stock
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    );
  }
  