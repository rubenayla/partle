import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/index.ts";

export default function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [store, setStore] = useState(null);

  useEffect(() => {
    api.get(`/v1/products/${id}`).then((res) => {
      setProduct(res.data);
      if (res.data.store_id) {
        api.get(`/v1/stores/${res.data.store_id}`).then((resp) =>
          setStore(resp.data)
        );
      }
    });
  }, [id]);

  if (!product) return <p>Loading…</p>;

  return (
    <div className="w-full max-w-screen-2xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-3xl font-bold text-foreground">{product.name}</h1>
        <Link to="/" className="text-blue-600 hover:underline text-lg">
          ← Home
        </Link>
      </div>

      {product.description && <p className="mb-4 text-lg text-text-secondary">{product.description}</p>}

      {product.url && (
        <p className="mb-4">
          <a
            href={product.url}
            className="text-blue-600 underline text-lg"
            target="_blank"
            rel="noopener noreferrer"
          >
            {product.url}
          </a>
        </p>
      )}

      {product.price !== null && (
        <p className="mb-4 text-2xl font-semibold text-primary">Price: €{product.price}</p>
      )}

      {store && (
        <section className="mt-8 pt-6 border-t border-gray-300 dark:border-gray-700">
          <h2 className="text-2xl font-semibold text-foreground mb-3">Store Details</h2>
          <p className="mb-2 text-lg text-text-secondary">{store.name}</p>
          {store.lat && store.lon && (
            <p className="text-lg text-text-secondary">
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
    </div>
  );
}
