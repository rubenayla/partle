// frontend/src/pages/Stores.jsx
import { useEffect, useState } from "react";
import api from "../api";
import { Link } from "react-router-dom";

export default function Stores() {
  const [stores, setStores] = useState([]);
  const [openForm, setOpenForm] = useState(false);
  const [form, setForm]       = useState({ name: "", address: "", lat: 0, lon: 0 });

  useEffect(() => {
    api.get("/v1/stores/").then(res => setStores(res.data));
  }, []);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function createStore(e) {
    e.preventDefault();
    const { data } = await api.post("/v1/stores/", form);
    setStores(prev => [...prev, data]);
    setOpenForm(false);
    setForm({ name: "", address: "", lat: 0, lon: 0 });
  }

  return (
    <main className="p-4">
      <header className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-semibold">Stores</h1>
        <button onClick={() => setOpenForm(true)} className="bg-blue-600 text-white px-3 py-1 rounded">
          + Add store
        </button>
      </header>

      {stores.length === 0 && <p>No stores yet.</p>}
      <ul className="space-y-2">
        {stores.map(s => (
          <li key={s.id} className="border p-3 rounded">
            <strong>{s.name}</strong>
              <Link to={`/stores/${s.id}/products`} className="text-blue-600 hover:underline">
                <strong>{s.name}</strong>
              </Link>
            <div className="text-sm text-gray-600">{s.address}</div>
          </li>
        ))}
      </ul>

      {openForm && (
        <form
          onSubmit={createStore}
          className="fixed inset-0 bg-black/40 flex items-center justify-center"
        >
          <div className="bg-white p-6 rounded shadow space-y-3 w-80">
            <h2 className="text-lg font-medium">New store</h2>

            <input name="name"    placeholder="Name"    value={form.name}    onChange={handleChange} className="border p-2 w-full" />
            <input name="address" placeholder="Address" value={form.address} onChange={handleChange} className="border p-2 w-full" />
            <input name="lat"  type="number" step="any" placeholder="Latitude"  value={form.lat}  onChange={handleChange} className="border p-2 w-full" />
            <input name="lon"  type="number" step="any" placeholder="Longitude" value={form.lon}  onChange={handleChange} className="border p-2 w-full" />

            <div className="flex gap-2 justify-end">
              <button type="button" onClick={() => setOpenForm(false)} className="px-3 py-1">Cancel</button>
              <button className="bg-blue-600 text-white px-3 py-1 rounded">Save</button>
            </div>
          </div>
        </form>
      )}
    </main>
  );
}
