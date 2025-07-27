#!/bin/bash

echo "🚀 Setting up Legal QA System..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating .env file..."
    cp backend/env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your HUGGINGFACE_API_KEY"
    echo "   Get your API key from: https://huggingface.co/settings/tokens"
    echo ""
    echo "Press Enter when you've added your API key..."
    read
fi

# Check if API key is set
if grep -q "your_huggingface_api_key_here" backend/.env; then
    echo "❌ Please add your Hugging Face API key to backend/.env"
    echo "   Get your API key from: https://huggingface.co/settings/tokens"
    exit 1
fi

echo "✅ Environment variables configured"

# Build and start the application
echo "🔨 Building and starting the application..."
docker-compose up --build -d

echo ""
echo "🎉 Legal QA System is starting up!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
echo ""
echo "Happy coding! 🚀" 