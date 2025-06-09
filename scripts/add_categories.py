import sys
import os
import csv

# Add the parent folder to the Python path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_folder)

# Now you can import modules from the parent folder
from sql_db import DatabaseManager

with DatabaseManager() as db:
    # Create a database
    print("Creating category table")
    result = db.create_category_table()
    print(f"Result: {result}")

# Create Categories
categories = []
with open("scripts/categories.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        categories.append(row)

for category in categories:
    with DatabaseManager() as db:
        db.add_category(
            name=category['category'],
            main_area=category['main_area'],
        )

# Show categories
with DatabaseManager() as db:
    categories = db.get_categories()
    print("Categories:")
    for category in categories:
        print(
            f"- {category['name']} (ID: {category['id']}), "
            f"Main Area: {category['main_area']}"
        )
