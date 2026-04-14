"""
SeekSite Configuration
"""

import os

# Ollama API
OLLAMA_API_URL = "http://localhost:11434/api/chat"
OLLAMA_MODELS_URL = "http://localhost:11434/api/tags"
DEFAULT_MODEL = "llama3"

# Generation Settings
MAX_TOKENS = 100000
TEMPERATURE = 0.7
# Long timeout for large local models
STREAM_TIMEOUT = 300

# Server Settings
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True

# Conversation
MAX_HISTORY_MESSAGES = 10
