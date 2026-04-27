#!/usr/bin/env bash
set -o errexit

echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt

echo "Building frontend..."
cd ../frontend
npm install

# Set API URL for production build
export VITE_API_URL=${VITE_API_URL:-.}
npm run build

# Copy frontend build to Django static files
echo "Copying frontend build to Django static directory..."
rm -rf ../backend/staticfiles/dist
mkdir -p ../backend/staticfiles
cp -r dist ../backend/staticfiles/

echo "Collecting Django static files..."
cd ../backend
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Build complete!"

