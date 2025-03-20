#!/bin/bash

# Function to find an available port starting from 5012
find_available_port() {
    port=5012
    while lsof -i ":$port" >/dev/null 2>&1; do
        port=$((port + 1))
    done
    echo $port
}

# Change to the app directory
cd "$(dirname "$0")"

# Kill any existing Python processes running the app
pkill -f "python3 app.py"

# Find an available port
PORT=$(find_available_port)

# Update the port in app.py
sed -i.bak "s/port=[0-9]*/port=$PORT/" app.py
rm -f app.py.bak

echo "Starting Squaring Calculator..."
echo "Once the server starts, you can access the app at:"
echo "  • Computer: http://localhost:$PORT"
echo "  • Phone (same WiFi): http://$(ipconfig getifaddr en0):$PORT"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask app in the background
python3 app.py &

# Wait a moment for the server to start
sleep 2

# Open the webpage in the default browser
open "http://localhost:$PORT"

# Wait for the Python process to finish
wait
