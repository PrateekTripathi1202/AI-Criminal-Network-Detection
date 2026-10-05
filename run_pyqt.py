"""
Run Script for PyQt6 National Criminal Intelligence System (NCIS)
AI-Powered Criminal Network Analysis System
"""

import sys
import os

# Ensure project root is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from pyqt_app.app_main import run_app

if __name__ == "__main__":
    sys.exit(run_app())
