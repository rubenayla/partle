/**
 * @fileoverview MapView Component - Interactive map display for products and stores
 * @module pages/MapView
 */
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";

// Fix for missing marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

/**
 * Map result item with location data
 */
interface MapItem {
  /** Unique item identifier */
  id: number;
  /** Item name */
  name: string;
  /** Store identifier */
  storeId: number;
  /** Store name */
  storeName: string;
  /** Item price */
  price: number;
  /** Quantity in stock */
  qty: number;
  /** Latitude coordinate */
  lat: number;
  /** Longitude coordinate */
  lng: number;
}

/**
 * Props for the MapView component
 */
interface MapViewProps {
  /** Array of items to display on map */
  results: MapItem[];
  /** Array of store IDs to highlight */
  highlights?: number[];
}

/**
 * MapView Component - Interactive map display for products and stores
 * 
 * Displays search results on an interactive map with location markers.
 * Supports highlighting specific stores with different colored markers.
 * 
 * @param props - Component props
 * @returns JSX element containing the map
 * 
 * @example
 * ```tsx
 * function ProductMap() {
 *   const mapItems = [
 *     {
 *       id: 1,
 *       name: "iPhone 14",
 *       storeId: 1,
 *       storeName: "Apple Store",
 *       price: 799,
 *       qty: 5,
 *       lat: 40.4168,
 *       lng: -3.7038
 *     }
 *   ];
 *   
 *   return (
 *     <MapView 
 *       results={mapItems}
 *       highlights={[1]}
 *     />
 *   );
 * }
 * ```
 */
export default function MapView({ results, highlights = [] }: MapViewProps): JSX.Element {
  console.log("MapView loaded, results =", results);
  const center: [number, number] = [40.4168, -3.7038]; // Madrid

  return (
    <MapContainer
      center={center}
      zoom={12}
      style={{ height: "60vh", width: "100%", borderRadius: "0.5rem", boxShadow: "0 0 5px rgba(0,0,0,0.2)" }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {results.map((item) => {
        const isHighlighted = highlights.includes(item.storeId);

        return (
          <Marker
            key={item.id}
            position={[item.lat, item.lng]}
            icon={
              isHighlighted
                ? L.icon({
                    iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png",
                    shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41],
                  })
                : undefined // use default icon
            }
          >
            <Popup>
              <div className="text-sm">
                <div className="font-semibold">{item.storeName}</div>
                <div className="text-gray-600">{item.name}</div>
                <div className="mt-1">
                  €{item.price.toFixed(2)} • {item.qty} in stock
                </div>
              </div>
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}