import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import api from "../api/index.ts";
import { Helmet } from "react-helmet-async";

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

      <header className="flex justify-between mb-4">
        <h1 className="text-2xl font-semibold">{product.name}</h1>
        
      </header>

      {product.image_url && (
        <img
          src={product.image_url}
          alt={product.name}
          className="w-full max-w-sm h-auto object-cover rounded mb-4"
        />
      )}

      {product.description && <p className="mb-3">{product.description}</p>}

      {product.url && (
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
      )}

      {product.price !== null && (
        <p className="mb-3">Price: €{product.price}</p>
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
