#!/usr/bin/env python3
"""
SC Chatbot Startup Script

This script sets up the Python path correctly and imports the FastAPI app.
Run this to start the backend server.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add backend parent directory to path
backend_parent = os.path.dirname(os.path.abspath(__file__))
if backend_parent not in sys.path:
    sys.path.insert(0, backend_parent)

# Change to backend directory for relative imports
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Now import the app - this will import all relative imports correctly
from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)