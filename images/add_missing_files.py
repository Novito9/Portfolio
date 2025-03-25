import os
import json
from pathlib import Path

# Path to your images folder
images_folder = Path(r"C:\Users\9\Documents\Novito9\Portfolio\images")

# Path to your JSON file
json_file = Path(r"C:\Users\9\Documents\Novito9\Portfolio\images\image-list.json")

# Function to generate default metadata for a file
def generate_default_metadata(file_name):
    return {
        "url": f"images/{file_name}",
        "alt": "Ai Generation Artwork",
        "title": file_name.split(".")[0],  # Use the file name (without extension) as the title
        "desc": "Prompt: Default description for the image.",/{file_name}"
    }

# Load the JSON list
with open(json_file, "r", encoding="utf-8") as f:
    image_list = json.load(f)

# Get the list of files already in the JSON list
existing_files = {item["url"].split("/")[-1] for item in image_list}

# Scan the images folder for missing files
added_files = []
for file_path in images_folder.iterdir():
    if file_path.is_file() and file_path.name not in existing_files:
        # Generate metadata for the missing file
        metadata = generate_default_metadata(file_path.name)
        image_list.append(metadata)
        added_files.append(file_path.name)
        print(f"Added: {file_path.name}")

# Save the updated JSON list
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(image_list, f, indent=2)

print(f"Added {len(added_files)} files to the JSON list.")