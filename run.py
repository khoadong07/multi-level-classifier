"""Entry point for the SPX Classification System"""
import sys
from pathlib import Path

# Add app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import and run the Streamlit app
from app.main import *
