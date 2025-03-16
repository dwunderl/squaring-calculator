#!/bin/bash

# Change to the app directory
cd "$(dirname "$0")"

# Get the local IP address
IP=$(ipconfig getifaddr en0)

# Print instructions
echo "Starting Squaring Calculator..."
echo "Once the server starts, you can access the app at:"
echo "  • Computer: http://localhost:5012"
echo "  • Phone (same WiFi): http://$IP:5012"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask app
python3 app.py
