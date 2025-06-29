"""
Module: main.py

This is the entry point for the Flask application.

How to use:
    From the base directory of the project, run the application using:
    `python -m app.main`

Dependencies:
    - app (the application factory in __init__.py)
"""

# Custom imports
from app import create_app


# Register the filter with Flask
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
