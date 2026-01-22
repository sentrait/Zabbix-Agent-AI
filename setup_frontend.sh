#!/bin/bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

nvm install --lts
nvm use --lts

# Install Vite project
npm create vite@latest frontend -- --template react

# Install dependencies
cd frontend
npm install
npm install lucide-react framer-motion tailwindcss postcss autoprefixer axios react-router-dom recharts

# Initialize Tailwind
npx tailwindcss init -p
