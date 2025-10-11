import sqlite3
import csv
import os

# Path to the database (update if needed)
db_path = os.path.join(os.path.dirname(__file__), '..', 'videos.db')
# Output CSV path
default_csv_path = os.path.join(os.path.dirname(__file__), 'videos_export.csv')


def export_videos_to_csv(db_file=db_path, csv_file=default_csv_path):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    query = "SELECT id, name, url_480 FROM videos"
    cursor.execute(query)
    rows = cursor.fetchall()

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'url_480'])
        writer.writerows(rows)

    print(f"Exported {len(rows)} videos to {csv_file}")
    conn.close()


if __name__ == "__main__":
    export_videos_to_csv()
