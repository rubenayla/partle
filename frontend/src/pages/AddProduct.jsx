// frontend/src/pages/AddProduct.jsx
import { useEffect, useState } from "react";
import api from "../api";

export default function AddProduct() {
  const [stores, setStores] = useState([]);
  const [form, setForm] = useState({
    name: "",
    spec: "",
    price: 0,
    url: "",
    description: "",
    store_id: "",
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api.get("/v1/stores/").then((res) => setStores(res.data));
  }, []);

  const change = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const save = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.post("/v1/products", { ...form, store_id: form.store_id || null });
      window.location.href = "/";
    } catch (err) {
      alert("Could not create product");
    } finally {
      setSaving(false);
    }
  };

  return (
    <main className="w-full max-w-screen-2xl mx-auto px-4">
      <header className="flex justify-between mb-4">
        <h1 className="text-2xl font-semibold">Add product</h1>
      </header>
      <form onSubmit={save} className="space-y-3 max-w-md">
        <input
          name="name"
          value={form.name}
          onChange={change}
          placeholder="Name"
          className="input border p-2 w-full"
        />
        <input
          name="spec"
          value={form.spec}
          onChange={change}
          placeholder="Spec"
          className="input border p-2 w-full"
        />
        <input
          name="price"
          type="number"
          step="any"
          value={form.price}
          onChange={change}
          placeholder="Price"
          className="input border p-2 w-full"
        />
        <input
          name="url"
          value={form.url}
          onChange={change}
          placeholder="URL (optional)"
          className="input border p-2 w-full"
        />
        <textarea
          name="description"
          value={form.description}
          onChange={change}
          placeholder="Description"
          className="input h-24 border p-2 w-full"
        />
        <select
          name="store_id"
          value={form.store_id}
          onChange={change}
          className="border p-2 w-full"
        >
          <option value="">Select store (optional)</option>
          {stores.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
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
