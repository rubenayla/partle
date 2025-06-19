import { useEffect, useState } from "react";
import api from "../api";

export default function Stores() {
  const [stores, setStores] = useState([]);

  useEffect(() => {
    api.get("/v1/stores").then(res => setStores(res.data));
  }, []);

  return (
    <ul className="p-4">
      {stores.map(s => (
        <li key={s.id} className="border p-2 mb-2 rounded">{s.name}</li>
      ))}
    </ul>
  );
}
