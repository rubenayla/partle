# Partle Project - Claude Notes

## 🚫 DO NOT ADD WITHOUT PERMISSION
- **NO new environment variables** without explicit user approval
- **NO new configuration systems** (no PRODUCTION_MODE, NODE_ENV, etc.)
- **NO complex environment detection** - keep it simple
- **NO new abstractions** that make debugging harder
- **NO new dependencies** without asking first

## 🚨 CRITICAL DATABASE WARNING 🚨
**ONLY ONE DATABASE EXISTS: Hetzner Production (91.98.68.236:5432/partle)**
**NEVER CREATE LOCAL DATABASES - USER EXPLICITLY FORBID THIS TWICE**
**ALWAYS VERIFY DATABASE_URL POINTS TO HETZNER BEFORE ANY DB OPERATION**

## ✅ ENVIRONMENT VARIABLES (COMPLETE LIST - DO NOT ADD MORE)
**Location**: Separate `.env` files for each service following industry best practices
- **Backend**: `backend/.env` - Private secrets (database, API keys)
- **Frontend**: `frontend/.env` - Build-time configuration (API base URL)
**Loading**: Each service loads its own `.env` with `override=True`

**Backend variables (backend/.env)**:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT signing key
- `CLOUDFLARE_WORKER_URL` - Email service endpoint
- `CLOUDFLARE_WORKER_API_KEY` - Email service authentication

**Frontend variables (frontend/.env)**:
- `VITE_API_BASE` - Backend API URL (build-time variable)

## Project Structure
- **Backend**: Python FastAPI application using UV for dependency management (fast, modern Python package manager)
- **Frontend**: React/TypeScript application using npm/Node.js
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic migrations

## Backend Commands (run from `/backend` directory)
- **Install dependencies**: `uv sync` (takes ~1 second!)
- **Run server**: `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- **Run migrations**: `uv run alembic upgrade head`
- **Create migration**: `uv run alembic revision -m "description"`
- **Check migration status**: `uv run alembic current`
- **Run Python scripts**: `uv run python <script>`
- **Add a package**: `uv add package-name`
- **Remove a package**: `uv remove package-name`

## Frontend Commands (run from `/frontend` directory)
- **Install dependencies**: `npm install`
- **Run dev server**: `npm run dev`
- **Run tests**: `npm test`
- **Build**: `npm run build`

## Key Files
- **Backend models**: `backend/app/db/models.py`
- **Backend schemas**: `backend/app/schemas/`
- **Alembic migrations**: `backend/alembic/versions/`
- **Backend config**: `backend/pyproject.toml` (works with UV)
- **Frontend config**: `frontend/package.json`

## Database Notes
- **PRODUCTION DATABASE ONLY**: postgresql://partle_user:[PASSWORD_FROM_ENV]@91.98.68.236:5432/partle
- Uses PostgreSQL enums for StoreType: 'physical', 'online', 'chain'
- Recent migration `6c21a37be6b8` added image storage fields (image_data, image_filename, image_content_type)
- SQLAlchemy models may need app restart after enum changes
- **NEVER USE localhost:5432 - ONLY HETZNER DATABASE**

## Production Server Access
- **Server IP**: 91.98.68.236 (Hetzner)
- **SSH User**: `deploy` (NOT ruben)
- **Application Path**: `/srv/partle/`
- **Backend Path**: `/srv/partle/backend/`
- **Frontend Path**: `/srv/partle/frontend/`
- **Environment Files**: `/srv/partle/backend/.env`
- **SSH Command**: `ssh deploy@91.98.68.236`
- **Deploy Process**: `git pull` then `sudo systemctl restart partle-backend partle-frontend`

## 🔐 Secrets Management & Security Rules
### Required Secrets
- **DATABASE_URL**: PostgreSQL connection string with rotated password
- **SECRET_KEY**: Backend JWT/session signing key (rotate regularly)
- **CLOUDFLARE_WORKER_API_KEY**: Email service authentication

### Storage Rules
- **Production Environment Files**:
  - `frontend/.env`: Frontend build config (VITE_API_BASE) - can be tracked in git (no secrets)
  - `backend/.env`: Backend secrets (DATABASE_URL, SECRET_KEY, etc.) - gitignored
- **Local Development**:
  - `frontend/.env`: Default development values (can be tracked)
  - `frontend/.env.local`: Local overrides (gitignored, takes precedence)
  - `backend/.env`: Backend secrets (gitignored)
  - **IMPORTANT**: Never create `.env.local` on production server
- **All `.env*` and `*.local` files are gitignored** - except `.env.example`
- **Local Testing**: Use `.env.test` for test database credentials (also gitignored)
- **Validation**: Always verify `DATABASE_URL` points to Hetzner before DB operations

### 🚨 CRITICAL: Never Hardcode Credentials 🚨
- **NEVER** put actual passwords, API keys, or SECRET_KEYs directly in Python/JS files
- **NEVER** use `os.environ.setdefault()` with real credential values
- **ALWAYS** load credentials from .env files using python-dotenv or similar
- **Test scripts** must read from environment, not have embedded credentials
- **Example files** should use placeholders like "your-api-key-here"
- **Before every commit**: Check for hardcoded credentials with grep
- **This applies to ALL AI assistants** (Opus, Sonnet, Haiku) - no exceptions

### Incident Response
- **If credentials are exposed**: Rotate ALL affected secrets immediately
- **Credential Rotation**: Update ALL environment files and restart services
- **Notify user** immediately of any credential exposure

## Image Storage System
- **Storage Method**: Binary data (BYTEA) stored directly in PostgreSQL database
- **Database Fields**: 
  - `image_data` (BYTEA): Binary image content
  - `image_filename` (VARCHAR): Original filename
  - `image_content_type` (VARCHAR): MIME type (e.g., 'image/jpeg')
- **API Serving**: `/v1/products/{id}/image` endpoint serves images with proper headers
- **Scraper Integration**: Scrapy pipeline downloads images and stores in database
- **Frontend Access**: Uses `getProductImageSrc()` utility to generate API URLs

## Testing
- **Backend**: pytest (check for test commands in pyproject.toml)
- **Frontend**: Vitest (configured in vite.config.js)
- **Search Engine**: `uv run python test_search_quick.py` (quick verification)
- **Search Tests**: `uv run pytest app/tests/test_search_simple.py -v` (comprehensive)

## Development Server Architecture

### **🏗️ Port Configuration (DO NOT CHANGE)**
This project uses a **decoupled frontend/backend architecture** with standard industry ports:

**Frontend Development Server:**
- **Port**: `3000` (React/Vite standard)
- **URL**: `http://localhost:3000`
- **Purpose**: Serves React app, hot-reload, development tools
- **Start Command**: `npm run dev -- --port 3000` (from `/frontend` directory)

**Backend API Server:**
- **Port**: `8000` (FastAPI standard)
- **URL**: `http://localhost:8000` 
- **Purpose**: API endpoints, database operations, image serving
- **Start Command**: `poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` (from `/backend` directory)

**Database Server (PostgreSQL):**
- **Port**: `5432` (PostgreSQL standard)
- **URL**: `postgresql://[user]:[password]@localhost:5432/partle`
- **Purpose**: Data storage, product/store/user persistence
- **Note**: Standard PostgreSQL port used by all clients, tools, and documentation

### **🔄 How They Connect:**
- Frontend (`3000`) makes HTTP requests to Backend (`8000`)
- Backend (`8000`) connects to Database (`5432`)
- Configuration: `frontend/.env.local` contains `VITE_API_BASE=http://localhost:8000`
- **Image URLs**: `http://localhost:8000/v1/products/{id}/image`
- **API Docs**: `http://localhost:8000/docs`

### **✅ Why This Setup:**
1. **Industry Standard**: React (3000) + FastAPI (8000) + PostgreSQL (5432) is the expected pattern
2. **Independent Development**: Frontend/backend can be developed separately
3. **Production Ready**: Can deploy to different services (Hetzner, AWS, etc.)
4. **Multiple Clients**: Same API can serve web, mobile, other apps
5. **Hot Reload**: Frontend changes don't restart API server
6. **Tool Compatibility**: All PostgreSQL clients expect port 5432

### **🚨 Port Troubleshooting:**
- **Frontend not on 3000**: Vite may use 5173 as fallback - always specify `--port 3000`
- **API not on 8000**: Check if port is occupied, use `netstat -tlnp | grep :8000`
- **CORS Errors**: 
  - Ensure `VITE_API_BASE` in `.env.local` matches backend URL
  - Backend CORS allows: `http://localhost:3000`, `http://localhost:5173` 
  - If changing ports, update CORS origins in `backend/app/main.py`

## 🚨 CRITICAL: Authentication Design - NO SEPARATE REGISTER/LOGIN 🚨
- **SINGLE AUTH PAGE ONLY** - No separate register and login pages
- **One endpoint** `/v1/auth/login` that:
  - Logs in existing users with correct password
  - Automatically creates account for new emails
  - Returns same JWT token response either way
- **Why**: Having two pages asking for the exact same data (email/password) is absurd UX
- **Frontend**: Single form, single submit, no "Sign Up" vs "Login" confusion
- **Backend**: Check if user exists → verify password OR create new account
- **NEVER suggest "Sign Up first"** - The system handles this automatically

## API Standards
- **NO trailing slash** for API endpoints: `/v1/stores`, `/v1/products`, `/v1/auth` (FastAPI standard)
- **Base URL**: `http://localhost:8000` (from VITE_API_BASE in .env.local)
- **Image Endpoints**: `/v1/products/{id}/image` serve binary image data from database
- **Note**: Production accepts both `/endpoint` and `/endpoint/` but canonical form is without trailing slash

## TypeScript & Module Standards
- **Use TypeScript** (.ts/.tsx) everywhere, never JavaScript
- **Use ESM only**: Always use ES Modules (import/export), never CommonJS (require/module.exports)
- **Exception**: Root config files (vite.config.js, tailwind.config.js, postcss.config.js, eslint.config.js)
- **Import types explicitly**: `import type { User } from '../types'` for type-only imports
- **Use proper JSDoc**: Include `@fileoverview`, `@param`, `@returns`, `@example` in all functions
- **Define interfaces**: Create comprehensive interfaces in `src/types/index.ts` for all data structures
- **Type API responses**: All API functions must have proper TypeScript return types
- **Avoid `any`**: Use specific types, `unknown`, or proper generics instead
- **Export types**: Always export interfaces and types for reuse across the application

## TypeScript Code Examples
- **Hook with proper typing**:
```tsx
import type { User } from '../types';

export function useAuth(): {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
} {
  // Implementation
}
```

- **API function with types**:
```tsx
import type { Product, PaginatedResponse } from '../types';

export async function getProducts(params: ProductSearchParams): Promise<PaginatedResponse<Product>> {
  // Implementation
}
```

- **Component props interface**:
```tsx
interface ProductCardProps {
  product: Product;
  onEdit?: (product: Product) => void;
  className?: string;
}

export function ProductCard({ product, onEdit, className }: ProductCardProps) {
  // Implementation
}
```

## Claude MCP (Model Context Protocol) Servers - LOCAL ONLY

### ✅ CORRECT MCP CONFIGURATION FOR CLAUDE DESKTOP
MCP servers allow Claude Desktop to interact with local tools and APIs. These run on your local machine, NOT on production servers.

**Working Configuration in `.mcp.json`:**
```json
{
  "mcpServers": {
    "partle-products": {
      "command": "poetry",
      "args": ["run", "-C", "/home/rubenayla/repos/partle/backend", "python", "/home/rubenayla/repos/partle/backend/scripts/run_mcp_products.py"],
      "env": {
        "PARTLE_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

**Key Requirements for Poetry-based MCP servers:**
1. **Use absolute paths** - Both for `-C` flag and script path
2. **Use `-C` flag** - Tells Poetry where to find `pyproject.toml`
3. **No `cwd` field needed** - The `-C` flag handles the directory
4. **Command is just `poetry`** - Not a shell script or wrapper

**What DOESN'T work:**
- Relative paths like `./backend` or `scripts/run.py`
- Using `cwd` field without `-C` flag
- Shell script wrappers (permission issues)
- Missing the `-C` flag (causes "Poetry could not find a pyproject.toml" error)

**Local MCP Server Files (Claude Desktop only):**
- **Configuration**: `/home/rubenayla/repos/partle/.mcp.json` (project-scoped)
- **Launch Scripts**: `/home/rubenayla/repos/partle/backend/scripts/run_mcp_*.py`
- **Server Code**: `/home/rubenayla/repos/partle/backend/app/mcp/`
- **Debug Logs**: `/home/rubenayla/.cache/claude-cli-nodejs/-home-rubenayla-repos-partle/mcp-logs-*/`
- **Settings**: `/home/rubenayla/repos/partle/.claude/settings.local.json`

**Available MCP Servers (local Claude Desktop tools):**
- `partle-products` - Product management
- `partle-stores` - Store management
- `partle-analytics` - Analytics tools
- `partle-price-intelligence` - Price analysis
- `partle-location-intelligence` - Location services
- `partle-recommendations` - Recommendation engine
- `partle-scraper-monitor` - Scraper monitoring

**Testing MCP Servers:**
```bash
cd /home/rubenayla/repos/partle/backend
poetry run python test_mcp.py
```

**Enable in Claude Desktop:**
1. Set `enableAllProjectMcpServers: true` in `.claude/settings.local.json`
2. Run `/mcp` command in Claude to see status
3. Servers should show as "connected" not "failed"

## Search Engine
- **Elasticsearch** for scalable search (millions of products)
- **Setup**: `docker compose up -d elasticsearch && poetry run python manage_search.py setup`
- **New endpoint**: `/v1/search/products/` with advanced filtering
- **Fallback**: `/v1/products/` uses database search if Elasticsearch unavailable

## Layout Architecture
- **Layout Component** (`frontend/src/components/Layout.tsx`): Global wrapper used ONLY at App level
- **App.tsx** wraps entire Router with `<Layout>` - provides SearchBar, spacing, container
- **Individual pages** should NEVER import or use Layout directly - they're already inside it
- **Fixed SearchBar** requires `mt-[72px] pt-4` spacing: 72px margin clears SearchBar + 16px padding
- **Container**: `max-w-screen-2xl mx-auto px-4` provides consistent width and horizontal padding

### CRITICAL: Avoid Nested Layouts
Pages like AddProduct, AddStore should use React fragments (`<>`) not `<Layout>` to prevent:
- Duplicate main elements
- Inconsistent spacing
- Visual layout issues