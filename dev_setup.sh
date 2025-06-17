#!/usr/bin/env bash

# Partle setup script based on README instructions
set -e

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
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
else
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
fi

PY_VERSION="3.12.3"
if ! pyenv versions --bare | grep -q "$PY_VERSION"; then
    pyenv install "$PY_VERSION"
fi

cd backend
pyenv local "$PY_VERSION"
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .

echo "Setup complete. Activate the virtualenv with 'source backend/.venv/bin/activate'"
