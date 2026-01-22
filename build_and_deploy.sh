#!/bin/bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

echo "Building Frontend..."
cd frontend
npm install
npm run build

echo "Deploying to Backend..."
cd ..
rm -rf backend/static
cp -r frontend/dist backend/static

echo "Done."
