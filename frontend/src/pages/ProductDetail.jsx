import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/index.ts";
import { Helmet } from "react-helmet-async";
import { useAuth } from "../hooks/useAuth.jsx";

export default function ProductDetail() {
  console.log("ProductDetail: Component mounting");
  const { id } = useParams();
  const { user, isLoading: authLoading } = useAuth();
  console.log("ProductDetail: useParams ID:", id, "authLoading:", authLoading, "user:", user?.email || "not logged in");
  const [product, setProduct] = useState(null);
  const [store, setStore] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editForm, setEditForm] = useState({
    name: "",
    description: "",
    price: "",
    url: "",
    image_url: ""
  });
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    console.log("ProductDetail: Loading product with ID:", id);
    if (!id) {
      console.error("ProductDetail: No product ID provided");
      return;
    }
    
    api.get(`/v1/products/${id}/`)
      .then((res) => {
        console.log("ProductDetail: Successfully loaded product:", res.data.name);
        setProduct(res.data);
        setEditForm({
          name: res.data.name || "",
          description: res.data.description || "",
          price: res.data.price || "",
          url: res.data.url || "",
          image_url: res.data.image_url || ""
        });
        if (res.data.store_id) {
          api.get(`/v1/stores/${res.data.store_id}/`).then((resp) =>
            setStore(resp.data)
          );
        }
      })
      .catch((error) => {
        console.error("ProductDetail: Error fetching product:", error);
        if (error.response?.status === 404) {
          console.error("ProductDetail: Product not found, ID:", id);
        }
      });
  }, [id]);

  const handleSave = async () => {
    setIsSaving(true);
    try {
      const updateData = {
        name: editForm.name,
        description: editForm.description || null,
        price: editForm.price ? parseFloat(editForm.price) : null,
        url: editForm.url || null,
        image_url: editForm.image_url || null
      };
      
      const response = await api.patch(`/v1/products/${id}/`, updateData);
      setProduct(response.data);
      setIsEditing(false);
    } catch (error) {
      console.error("Failed to update product:", error);
      alert("Failed to update product. Please try again.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    setEditForm({
      name: product.name || "",
      description: product.description || "",
      price: product.price || "",
      url: product.url || "",
      image_url: product.image_url || ""
    });
    setIsEditing(false);
  };

  const isOwner = user && product && user.id === product.creator_id;

  if (!product) return <p>Loading…</p>;
  if (authLoading) return <p>Loading…</p>;

  const productSchema = {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": product.name,
    "description": product.description || product.name,
    "image": product.image_url || "",
    "url": `https://partle.vercel.app/products/${product.id}`,
    "offers": {
      "@type": "Offer",
      "priceCurrency": "EUR",
      "price": product.price,
      "itemCondition": "https://schema.org/NewCondition",
      "availability": "https://schema.org/InStock",
      "seller": {
        "@type": "Organization",
        "name": store ? store.name : "Partle",
      },
    },
  };

  return (
    <main className="w-full max-w-screen-2xl mx-auto px-4">
      <Helmet>
        <title>{product.name} - Partle</title>
        <meta name="description" content={product.description || product.name} />
        <script type="application/ld+json">
          {JSON.stringify(productSchema)}
        </script>
      </Helmet>

      <header className="flex justify-between items-start mb-4">
        {isEditing ? (
          <input
            type="text"
            value={editForm.name}
            onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
            className="text-2xl font-semibold bg-transparent border-b border-gray-300 focus:border-blue-500 focus:outline-none flex-1 mr-4"
            placeholder="Product name"
          />
        ) : (
          <h1 className="text-2xl font-semibold">{product.name}</h1>
        )}
        
        {isOwner && (
          <div className="flex gap-2">
            {isEditing ? (
              <>
                <button
                  onClick={handleSave}
                  disabled={isSaving || !editForm.name.trim()}
                  className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                >
                  {isSaving ? "Saving..." : "Save"}
                </button>
                <button
                  onClick={handleCancel}
                  disabled={isSaving}
                  className="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700 disabled:opacity-50"
                >
                  Cancel
                </button>
              </>
            ) : (
              <button
                onClick={() => setIsEditing(true)}
                className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
              >
                Edit
              </button>
            )}
          </div>
        )}
      </header>

      {isEditing ? (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Image URL
          </label>
          <input
            type="url"
            value={editForm.image_url}
            onChange={(e) => setEditForm({ ...editForm, image_url: e.target.value })}
            className="w-full p-2 border border-gray-300 rounded focus:border-blue-500 focus:outline-none"
            placeholder="https://example.com/image.jpg"
          />
          {editForm.image_url && (
            <img
              src={editForm.image_url}
              alt="Preview"
              className="w-full max-w-sm h-auto object-cover rounded mt-2"
              onError={(e) => {
                e.target.style.display = 'none';
              }}
            />
          )}
        </div>
      ) : (
        product.image_url && (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full max-w-sm h-auto object-cover rounded mb-4"
          />
        )
      )}

      {isEditing ? (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            value={editForm.description}
            onChange={(e) => setEditForm({ ...editForm, description: e.target.value })}
            className="w-full p-2 border border-gray-300 rounded focus:border-blue-500 focus:outline-none"
            rows="3"
            placeholder="Product description"
          />
        </div>
      ) : (
        product.description && <p className="mb-3">{product.description}</p>
      )}

      {isEditing ? (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Product URL
          </label>
          <input
            type="url"
            value={editForm.url}
            onChange={(e) => setEditForm({ ...editForm, url: e.target.value })}
            className="w-full p-2 border border-gray-300 rounded focus:border-blue-500 focus:outline-none"
            placeholder="https://example.com/product"
          />
        </div>
      ) : (
        product.url && (
          <p className="mb-3">
            <a
              href={product.url}
              className="text-blue-600 underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              {product.url}
            </a>
          </p>
        )
      )}

      {isEditing ? (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Price (€)
          </label>
          <input
            type="number"
            step="0.01"
            value={editForm.price}
            onChange={(e) => setEditForm({ ...editForm, price: e.target.value })}
            className="w-full p-2 border border-gray-300 rounded focus:border-blue-500 focus:outline-none"
            placeholder="0.00"
          />
        </div>
      ) : (
        product.price !== null && (
          <p className="mb-3">Price: €{product.price}</p>
        )
      )}

      {store && (
        <section className="mt-6 border-t pt-4">
          <h2 className="font-medium">Store</h2>
          <p className="mb-1">{store.name}</p>
          {store.lat && store.lon && (
            <p>
              {store.lat}, {store.lon} –{' '}
              <a
                href={`https://maps.google.com/?q=${store.lat},${store.lon}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 underline"
              >
                View on Google Maps
              </a>
            </p>
          )}
        </section>
      )}
    </main>
  );
}
