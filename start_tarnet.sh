#!/bin/bash

# Start TARNet System - WebSocket Server + Web Client

echo "=== Starting TARNet System ==="
echo "Starting WebSocket Server (backend) and Web Client (frontend)"
echo

# Function to cleanup background processes on exit
cleanup() {
    echo "Stopping TARNet services..."
    if [ ! -z "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null
    fi
    exit 0
}

# Set cleanup trap
trap cleanup SIGINT SIGTERM

# Start WebSocket Server in background
echo "Starting WebSocket Server on localhost:8000..."
cd tarnet/server
python server.py &
SERVER_PID=$!
cd ../..

# Wait a moment for server to start
sleep 2

# Start Flask Web Client (foreground - this is the main service)
echo "Starting Web Client on 0.0.0.0:5000..."
echo "Frontend will be available for users on port 5000"
echo
cd tarnet/client
python app.py

# This will only reach if Flask exits
cleanup