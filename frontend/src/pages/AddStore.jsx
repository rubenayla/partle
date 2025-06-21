// frontend/src/pages/AddStore.jsx
import { useState } from "react";
import api from "../api";

export default function AddStore() {
  const [form, setForm] = useState({ name: "", address: "", lat: 0, lon: 0 });
  const [saving, setSaving] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.post("/v1/stores/", { ...form, type: "physical" });
      window.location.href = "/stores";
    } catch (err) {
      alert("Could not create store");
    } finally {
      setSaving(false);
    }
  };

  return (
    <main className="w-full max-w-screen-2xl mx-auto px-4">
      <header className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-semibold">Add store</h1>
      </header>
      <form onSubmit={handleSubmit} className="space-y-3 max-w-md">
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Name"
          className="border p-2 w-full"
        />
        <input
          name="address"
          value={form.address}
          onChange={handleChange}
          placeholder="Address"
          className="border p-2 w-full"
        />
        <input
          name="lat"
          type="number"
          step="any"
          value={form.lat}
          onChange={handleChange}
          placeholder="Latitude"
          className="border p-2 w-full"
        />
        <input
          name="lon"
          type="number"
          step="any"
          value={form.lon}
          onChange={handleChange}
          placeholder="Longitude"
          className="border p-2 w-full"
        />
        <button
          disabled={saving}
          className="bg-blue-600 text-white px-3 py-1 rounded"
        >
          {saving ? "Saving..." : "Save"}
        </button>
      </form>
    </main>
  );
}
