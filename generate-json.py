import os
import json
from pathlib import Path

# Configuration
IMAGE_FOLDER = "images"  # Folder containing images
OUTPUT_FILE = "images/image-list.json"  # Output JSON file
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}  # Allowed image formats

def generate_image_list():
    images = []
    
    # Loop through files in the image folder
    for file in Path(IMAGE_FOLDER).iterdir():
        if file.suffix.lower() in ALLOWED_EXTENSIONS:  # Fixed variable name
            filename = file.name
            clean_name = filename.split(".")[0].replace("_", " ").replace("-", " ")
            
            images.append({
                "url": f"{IMAGE_FOLDER}/{filename}",
                "alt": clean_name,
                "title": clean_name.title(),
                "desc": f"AI-generated artwork: {clean_name}"
            })
    
    # Save to JSON file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(images, f, indent=2)
    
    print(f"✅ Generated {OUTPUT_FILE} with {len(images)} images.")

if __name__ == "__main__":
    generate_image_list()