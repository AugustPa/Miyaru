import csv
import os
import requests
from urllib.parse import urlparse

CSV_PATH = "/Volumes/AugustMV25B/miyaru cs apr23-apr24.csv"    # Path to your CSV
OUTPUT_FOLDER = "downloaded_photos" # Where images will be stored

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

with open(CSV_PATH, "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        # row["image_url"] might contain multiple URLs separated by newlines/spaces.
        raw_urls = row["File Upload"]
        if not raw_urls:
            continue

        # Normalize newline -> space, then split on whitespace:
        raw_urls = raw_urls.replace("\n", " ")
        links = raw_urls.split()  # splits on any whitespace

        # If you notice some missing slash (like "https:/"), you can fix it:
        # e.g. if link starts with "https:/" but not "https://", replace it
        def fix_url(link):
            if link.startswith("https:/") and not link.startswith("https://"):
                return link.replace("https:/", "https://", 1)
            return link

        links = [fix_url(link) for link in links]

        # Now download each link separately
        for link in links:
            try:
                response = requests.get(link, timeout=10)
                response.raise_for_status()

                # Determine filename
                parsed_url = urlparse(link)
                filename = os.path.basename(parsed_url.path)
                
                # If you want to add e.g. row['id']:
                # filename = f"{row['id']}_{filename}"

                # Save it
                path = os.path.join(OUTPUT_FOLDER, filename)
                with open(path, "wb") as f:
                    f.write(response.content)
                
                print(f"Downloaded: {filename}")

            except requests.exceptions.RequestException as e:
                # Connection issues, 404, etc.
                print(f"Failed to download {link} - {e}")