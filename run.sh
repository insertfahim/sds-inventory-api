#!/bin/bash

echo "Building Docker containers..."
docker-compose build

echo "Starting services..."
docker-compose up -d

echo "Waiting for API to be ready..."
sleep 10

# Check if API is available
if curl -f http://localhost:8000/docs > /dev/null 2>&1; then
    echo "✅ API is available at http://localhost:8000"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo "🔄 Alternative docs: http://localhost:8000/redoc"
else
    echo "❌ API is not responding. Check logs with: docker-compose logs api"
fi

echo "To stop services: docker-compose down"