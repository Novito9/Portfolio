import os
import json
from pathlib import Path

# Path to your images folder
images_folder = Path(r"C:\Users\9\Documents\Novito9\Portfolio\images")

# Path to your JSON file
json_file = Path(r"C:\Users\9\Documents\Novito9\Portfolio\images\image-list.json")

# Load the JSON list
with open(json_file, "r", encoding="utf-8") as f:
    image_list = json.load(f)

# Filter out entries for missing files
updated_image_list = []
for item in image_list:
    old_name = item["url"].split("/")[-1]  # Extract file name from URL
    old_path = images_folder / old_name

    if old_path.exists():
        updated_image_list.append(item)
    else:
        print(f"Removed entry for missing file: {old_name}")

# Save the updated JSON list
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(updated_image_list, f, indent=2)

print("JSON list updated successfully.")