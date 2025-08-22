#!/usr/bin/python3.10

import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/minds-eye-photography'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set up the Flask app
sys.path.insert(0, os.path.join(project_home, 'src'))

from main import app as application

if __name__ == "__main__":
    application.run()

