#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Flask application entry point
from flask import Flask, request, jsonify
import os
from services import process_chat_request

app = Flask(__name__)

# Enable CORS - Add headers to skip CORS issues
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Load environment variables
# NOTE: Assuming environment variables are set up in a .env file that the container/host environment loads
# For local development, set variables like OLLAMA_API_URL, OLLAMA_MODEL, etc.

@app.route('/', methods=['GET'])
def health_check():
    """Basic route for health check."""
    return jsonify({"status": "ok", "message": "AI Chatbot Backend is running successfully."})

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """
    Endpoint to handle all chat messages from various platforms.
    Expected JSON body: {"senderId": "...", "messageText": "...", "platform": "..."}
    """
    data = request.get_json()
    
    if not data or not data.get('senderId') or not data.get('messageText'):
        return jsonify({"error": "Missing senderId or messageText."}), 400

    sender_id = data['senderId']
    message_text = data['messageText']
    platform = data.get('platform', 'unknown')

    print("[INFO] Received message from %s on platform %s: %s" % (sender_id, platform, message_text))

    try:
        # 1. Process the chat request through the core service
        response_text = process_chat_request(message_text, sender_id, platform)
        
        # 2. Simulate saving conversation history (placeholder)
        # save_conversation_history(sender_id, message_text, response_text) 
        
        # 3. Return response
        return jsonify({
            "success": True, 
            "response": response_text,
            "message": "Successfully processed request for %s" % sender_id
        })
    except Exception as e:
        print("Error processing chat request: %s" % e)
        return jsonify({"error": "Failed to process chat request."}), 500

if __name__ == '__main__':
    # Use a standard port
    port = int(os.environ.get("PORT", 3001))
    print("\n=====================================================")
    print("✅ Server running successfully on port %d" % port)
    print("   API Endpoint: http://localhost:%d/api/chat" % port)
    print("=====================================================\n")
    # Flask's run function handles the actual serving
    app.run(host='0.0.0.0', port=port)