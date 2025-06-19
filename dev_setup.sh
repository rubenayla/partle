#!/usr/bin/env bash
# dev_setup.sh — Partle unified setup script
set -e

echo "📦 Installing system dependencies..."

sudo apt update
sudo apt install -y \
  build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
  libsqlite3-dev libncurses-dev libffi-dev liblzma-dev uuid-dev \
  libgdbm-dev tk-dev libnss3-dev libdb-dev libexpat1-dev \
  libxml2-dev libxmlsec1-dev libx11-dev libxext-dev libxrender-dev \
  xz-utils \
  postgresql postgresql-contrib

# ---- Node.js via nvm ----
if ! command -v nvm >/dev/null 2>&1; then
    echo "⬇️ Installing nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
fi

export NVM_DIR="$HOME/.nvm"
# shellcheck source=/dev/null
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install --lts
nvm use --lts

# ---- Frontend ----
if [ ! -d frontend ]; then
    echo "⚛️  Creating frontend (Vite + React)..."
    npm create vite@latest frontend -- --template react
fi

cd frontend
npm install
npm install -D tailwindcss@^3 postcss autoprefixer
npx tailwindcss init -p
cd ..

# ---- Python backend ----
if ! command -v pyenv >/dev/null 2>&1; then
    echo "⬇️ Installing pyenv..."
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
fi

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

PY_VERSION="3.12.3"
if ! pyenv versions --bare | grep -q "$PY_VERSION"; then
    pyenv install "$PY_VERSION"
fi

cd backend
echo "$PY_VERSION" > .python-version

# ---- Poetry environment ----
if ! command -v poetry >/dev/null 2>&1; then
    echo "⬇️ Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi

poetry config virtualenvs.in-project true
poetry env use "$PY_VERSION"
poetry install

echo "✅ Partle setup complete. To activate the backend shell, run:"
echo "cd backend && poetry shell"
