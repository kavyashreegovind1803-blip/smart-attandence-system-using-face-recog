#!/bin/bash

echo "🚀 Deploying Smart Attendance System with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Stop and remove existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Services are running!"
    echo ""
    echo "🌐 Access the application at: http://localhost:5000"
    echo "🔑 Default admin credentials:"
    echo "   Username: admin"
    echo "   Password: admin123"
    echo ""
    echo "📊 MySQL is available at: localhost:3306"
    echo "   Database: attendance_system"
    echo "   Username: appuser"
    echo "   Password: apppassword"
    echo ""
    echo "🔧 To stop the application: docker-compose down"
    echo "📝 To view logs: docker-compose logs -f"
else
    echo "❌ Failed to start services. Check logs with: docker-compose logs"
    exit 1
fi