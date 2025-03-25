import os
import json
import re  # Import the re module
from pathlib import Path

# Path to your images folder
images_folder = Path(r"C:\Users\9\Documents\Novito9\Portfolio\images")

# Path to your JSON file
json_file = Path(r"C:\Users\9\Documents\Novito9\Portfolio\images\image-list.json")

# Function to generate a shorter name
def generate_short_name(old_name):
    # Remove special characters and spaces, and limit the length
    short_name = re.sub(r'[^a-zA-Z0-9-]', '-', old_name)  # Replace special characters with hyphens
    short_name = short_name[:40]  # Limit the length to 40 characters
    return f"{short_name}.jpg"

# Load the JSON list
with open(json_file, "r", encoding="utf-8") as f:
    image_list = json.load(f)

# Rename files and update JSON
for item in image_list:
    old_name = item["url"].split("/")[-1]  # Extract file name from URL
    old_path = images_folder / old_name

    if old_path.exists():
        new_name = generate_short_name(old_name)
        new_path = images_folder / new_name

        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} -> {new_name}")

        # Update the JSON entry
        item["url"] = f"images/{new_name}"
    else:
        print(f"File not found: {old_name}")

# Save the updated JSON list
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(image_list, f, indent=2)

print("JSON list updated successfully.")