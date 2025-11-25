#!/bin/bash

echo "======================================"
echo "Bus Booking System - Startup Script"
echo "======================================"
echo ""

echo "Checking if database needs seeding..."
if [ ! -f "backend/.seeded" ]; then
    echo "Seeding database (one-time setup)..."
    cd backend
    pip install -r requirements.txt
    python seed_data.py
    touch .seeded
    cd ..
    echo "Database seeded successfully!"
else
    echo "Database already seeded, skipping..."
fi

echo ""
echo "Starting backend with Docker..."
docker-compose up -d

echo ""
echo "Waiting for backend to be ready..."
sleep 5

echo ""
echo "Backend is running at http://localhost:8000"
echo ""
echo "To start the frontend, run:"
echo "  npm install"
echo "  npm run dev"
echo ""
echo "The frontend will be available at http://localhost:5173"
echo ""
echo "To stop the backend, run: docker-compose down"
echo "======================================"
