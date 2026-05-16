"""
SC Chatbot Backend Package

This package provides the backend API for the SC Chatbot platform.
"""

import sys
import os

# Add backend root to path for absolute imports
backend_root = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(backend_root) not in sys.path:
    sys.path.insert(0, os.path.dirname(backend_root))

from . import models
from . import rag
from . import services
from . import api