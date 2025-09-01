/**
 * @fileoverview Documentation page component for API and MCP server information
 * @module pages/Documentation
 */
import { Helmet } from 'react-helmet-async';

/**
 * Documentation Component - API and MCP server documentation
 * 
 * Provides comprehensive documentation for developers including:
 * - REST API endpoints and usage
 * - MCP server setup and integration
 * - Authentication and examples
 * - Interactive API documentation links
 * 
 * @returns JSX element containing the documentation page
 */
export default function Documentation(): JSX.Element {
  return (
    <div className="w-full">
      <Helmet>
        <title>Documentation - Partle API & MCP Server</title>
        <meta name="description" content="Developer documentation for Partle API endpoints and MCP server integration" />
      </Helmet>

      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Developer Documentation
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            API endpoints, MCP server setup, and integration guides for Partle
          </p>
        </header>

        {/* Quick Links */}
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-blue-900 dark:text-blue-100 mb-4">Quick Access</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <a
              href="/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
              Interactive API Docs (Swagger)
            </a>
            <a
              href="https://github.com/anthropics/claude-code"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 bg-gray-800 hover:bg-gray-900 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              MCP Documentation
            </a>
          </div>
        </div>

        <div className="space-y-8">
          {/* API Overview */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">REST API</h2>
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Base URL</h3>
                <code className="bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded text-sm">
                  http://localhost:8000/v1
                </code>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Products</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2">
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-mono">GET</span>
                      <code className="text-gray-700 dark:text-gray-300">/products/</code>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-mono">GET</span>
                      <code className="text-gray-700 dark:text-gray-300">/products/{"{id}"}/</code>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-mono">GET</span>
                      <code className="text-gray-700 dark:text-gray-300">/products/{"{id}"}/image</code>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-mono">POST</span>
                      <code className="text-gray-700 dark:text-gray-300">/products/</code>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs font-mono">PATCH</span>
                      <code className="text-gray-700 dark:text-gray-300">/products/{"{id}"}/</code>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Stores</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2">
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-mono">GET</span>
                      <code className="text-gray-700 dark:text-gray-300">/stores/</code>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-mono">GET</span>
                      <code className="text-gray-700 dark:text-gray-300">/stores/{"{id}"}/</code>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-mono">POST</span>
                      <code className="text-gray-700 dark:text-gray-300">/stores/</code>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-xs font-mono">PATCH</span>
                      <code className="text-gray-700 dark:text-gray-300">/stores/{"{id}"}/</code>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-6">
                <h4 className="font-semibold text-gray-900 dark:text-white mb-3">Search</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs font-mono">GET</span>
                    <code className="text-gray-700 dark:text-gray-300">/search/products/</code>
                    <span className="text-gray-500 text-xs">- Elasticsearch-powered search</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Authentication */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Authentication</h2>
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                Use JWT tokens for authenticated requests. Include the token in the Authorization header:
              </p>
              <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
                <code className="text-sm text-gray-800 dark:text-gray-200">
                  Authorization: Bearer YOUR_JWT_TOKEN
                </code>
              </div>
              <div className="mt-4 space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-mono">POST</span>
                  <code className="text-gray-700 dark:text-gray-300">/auth/login</code>
                  <span className="text-gray-500 text-xs">- Get JWT token</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs font-mono">POST</span>
                  <code className="text-gray-700 dark:text-gray-300">/auth/register</code>
                  <span className="text-gray-500 text-xs">- Create new account</span>
                </div>
              </div>
            </div>
          </section>

          {/* MCP Server */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">MCP Server</h2>
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
              <p className="text-gray-700 dark:text-gray-300 mb-4">
                The Partle MCP server provides tools for interacting with product and store data from Claude Code or other MCP clients.
              </p>
              
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Available Tools</h3>
                <div className="space-y-3">
                  <div className="border-l-4 border-blue-500 pl-4">
                    <h4 className="font-medium text-gray-900 dark:text-white">search_products</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Search for products with filters (query, price range, tags)</p>
                  </div>
                  <div className="border-l-4 border-green-500 pl-4">
                    <h4 className="font-medium text-gray-900 dark:text-white">get_product_details</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Get detailed information about a specific product</p>
                  </div>
                  <div className="border-l-4 border-purple-500 pl-4">
                    <h4 className="font-medium text-gray-900 dark:text-white">search_stores</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Find stores by name, type, or location</p>
                  </div>
                  <div className="border-l-4 border-orange-500 pl-4">
                    <h4 className="font-medium text-gray-900 dark:text-white">run_scrapers</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Execute web scrapers to collect new product data</p>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Configuration</h3>
                <p className="text-gray-700 dark:text-gray-300 mb-3">
                  Add this configuration to your MCP client settings:
                </p>
                <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg overflow-x-auto">
                  <pre className="text-sm text-gray-800 dark:text-gray-200">
{`{
  "mcpServers": {
    "partle": {
      "command": "python",
      "args": ["-m", "app.mcp_server"],
      "cwd": "/path/to/partle/backend"
    }
  }
}`}
                  </pre>
                </div>
              </div>
            </div>
          </section>

          {/* Example Usage */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Example Usage</h2>
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Search Products</h3>
                  <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
                    <code className="text-sm text-gray-800 dark:text-gray-200">
                      GET /v1/products/?q=drill&min_price=20&max_price=100&limit=10
                    </code>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Create Product</h3>
                  <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg overflow-x-auto">
                    <pre className="text-sm text-gray-800 dark:text-gray-200">
{`POST /v1/products/
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
  "name": "Power Drill",
  "description": "18V cordless drill with 2 batteries",
  "price": 89.99,
  "store_id": 1,
  "url": "https://store.com/drill"
}`}
                    </pre>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* Database Schema */}
          <section>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Data Schema</h2>
            <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Product</h3>
                  <div className="space-y-2 text-sm font-mono">
                    <div><span className="text-blue-600">id</span>: integer</div>
                    <div><span className="text-blue-600">name</span>: string</div>
                    <div><span className="text-blue-600">description</span>: string?</div>
                    <div><span className="text-blue-600">price</span>: decimal?</div>
                    <div><span className="text-blue-600">url</span>: string?</div>
                    <div><span className="text-blue-600">image_url</span>: string?</div>
                    <div><span className="text-blue-600">store_id</span>: integer</div>
                    <div><span className="text-blue-600">creator_id</span>: integer?</div>
                    <div><span className="text-blue-600">tags</span>: Tag[]</div>
                  </div>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Store</h3>
                  <div className="space-y-2 text-sm font-mono">
                    <div><span className="text-green-600">id</span>: integer</div>
                    <div><span className="text-green-600">name</span>: string</div>
                    <div><span className="text-green-600">type</span>: 'physical' | 'online' | 'chain'</div>
                    <div><span className="text-green-600">address</span>: string?</div>
                    <div><span className="text-green-600">latitude</span>: float?</div>
                    <div><span className="text-green-600">longitude</span>: float?</div>
                    <div><span className="text-green-600">website</span>: string?</div>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}