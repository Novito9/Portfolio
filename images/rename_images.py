import os
import json
import re
from pathlib import Path

# Path to your images folder
images_folder = Path(r"C:\Users\9\Documents\Novito9\Portfolio\images")

# Path to your JSON file
json_file = Path(r"C:\Users\9\Documents\Novito9\Portfolio\images\image-list.json")

# Function to generate a shorter name
def generate_short_name(old_name):
    # Extract the first few words or a unique identifier
    # Example: "Anubis-jackal-headed-god-towering-in-judgment-hall-holding-scales-and-ankh-souls-below.jpg" -> "Anubis_01.jpg"
    base_name = os.path.splitext(old_name)[0]  # Remove extension
    words = re.split(r'[-_]', base_name)  # Split by hyphen or underscore
    short_name = "_".join(words[:2])  # Use the first two words
    return f"{short_name}.jpg"

# Load the JSON list
with open(json_file, "r") as f:
    image_list = json.load(f)

# Rename files and update JSON
for i, item in enumerate(image_list):
    old_path = images_folder / item["url"].split("/")[-1]  # Extract file name from URL
    new_name = generate_short_name(old_path.name)
    new_path = images_folder / new_name

    # Rename the file
    if old_path.exists():
        os.rename(old_path, new_path)
        print(f"Renamed: {old_path.name} -> {new_name}")
    else:
        print(f"File not found: {old_path.name}")

    # Update the JSON entry
    item["url"] = f"images/{new_name}"

# Save the updated JSON list
with open(json_file, "w") as f:
    json.dump(image_list, f, indent=2)

print("JSON list updated successfully.")