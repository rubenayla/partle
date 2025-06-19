#!/usr/bin/env bash

# Partle setup script based on README instructions
set -e

# ---- System packages required for building Python ----
sudo apt update
sudo apt install -y \
  build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
  libsqlite3-dev libncurses-dev libffi-dev liblzma-dev uuid-dev \
  libgdbm-dev tk-dev libnss3-dev libdb-dev libexpat1-dev \
  libxml2-dev libxmlsec1-dev libx11-dev libxext-dev libxrender-dev \
  xz-utils

# ---- Node.js via nvm ----
if ! command -v nvm >/dev/null 2>&1; then
    echo "Installing nvm..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi

# ensure nvm is loaded
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

nvm install --lts
nvm use --lts

# ---- Frontend ----
if [ ! -d frontend ]; then
    npm create vite@latest frontend -- --template react
fi
cd frontend
npm install
# Tailwind CSS
npm install -D tailwindcss@^3 postcss autoprefixer
npx tailwindcss init -p
cd ..

# ---- Python backend ----
if ! command -v pyenv >/dev/null 2>&1; then
    echo "Installing pyenv..."
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
fi
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

PY_VERSION="3.12.3"
pyenv install -s "$PY_VERSION"
pyenv global "$PY_VERSION"

cd backend
rm -rf .venv
poetry config virtualenvs.in-project true
poetry env use "$(pyenv which python)"
poetry install

echo "Setup complete. Activate with 'poetry shell' inside backend/"
