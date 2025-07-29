// frontend/src/pages/Products.jsx
import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/index.ts";

export default function Products() {
  const { id } = useParams(); // store id
  const [products, setProducts] = useState([]);
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    name: "",
    spec: "",
    price: 0,
    url: "",
    description: "",
  });

  useEffect(() => {
    api.get(`/v1/products/store/${id}`).then((res) => setProducts(res.data));
  }, [id]);

  const change = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  async function save(e) {
    e.preventDefault();
    const { data } = await api.post("/v1/products", { ...form, store_id: id });
    setProducts((prev) => [...prev, data]);
    setOpen(false);
    setForm({ name: "", spec: "", price: 0, url: "", description: "" });
  }

  return (
    <main className="w-full max-w-screen-2xl mx-auto px-4">
      <header className="flex justify-between mb-4">
        <h1 className="text-2xl font-semibold">Products</h1>
        <Link to="/stores" className="text-blue-600 hover:underline">
          ← Back
        </Link>
      </header>

      <button
        onClick={() => setOpen(true)}
        className="bg-transparent text-foreground hover:bg-background border border-gray-300 dark:border-gray-600 px-3 py-1 rounded mb-4"
      >
        + Add product
      </button>

      {products.length === 0 && <p>No products yet.</p>}
      <ul className="space-y-2">
        {products.map((p) => (
          <li key={p.id} className="border p-3 rounded">
            <div className="flex items-center gap-4">
              {p.image_url && (
                <img
                  src={p.image_url}
                  alt={p.name}
                  className="w-16 h-16 object-cover rounded"
                />
              )}
              <div>
                <Link
                  to={`/products/${p.id}`}
                  className="text-blue-600 hover:underline"
                >
                  <strong>{p.name}</strong>
                </Link>{" "}
                — {p.spec ?? "–"} — €{p.price ?? "?"}
              </div>
            </div>
          </li>
        ))}
      </ul>

      {open && (
        <form
          onSubmit={save}
          className="fixed inset-0 bg-black/40 flex items-center justify-center"
        >
          <div className="bg-white p-6 rounded shadow space-y-3 w-96">
            <h2 className="text-lg font-medium">New product</h2>

            <input
              name="name"
              value={form.name}
              onChange={change}
              placeholder="Name"
              className="input"
            />
            <input
              name="spec"
              value={form.spec}
              onChange={change}
              placeholder="Spec"
              className="input"
            />
            <input
              name="price"
              type="number"
              step="any"
              value={form.price}
              onChange={change}
              placeholder="Price"
              className="input"
            />
            <input
              name="url"
              value={form.url}
              onChange={change}
              placeholder="URL (optional)"
              className="input"
            />
            <textarea
              name="description"
              value={form.description}
              onChange={change}
              placeholder="Description"
              className="input h-24"
            />

            <div className="flex gap-2 justify-end">
              <button type="button" onClick={() => setOpen(false)}>
                Cancel
              </button>
              <button className="bg-blue-600 text-white px-3 py-1 rounded">
                Save
              </button>
            </div>
          </div>
        </form>
      )}
    </main>
  );
}
