import json
import os
from datetime import datetime, timedelta
import random
from pathlib import Path

def generate_missing_info(image_data):
    """
    Generate missing information for image entries based on filename and other heuristics
    """
    # List of possible tags/categories
    possible_tags = [
        "nature", "technology", "art", "abstract", 
        "cyberpunk", "portrait", "landscape", "fantasy",
        "sci-fi", "concept", "digital", "illustration",
        "photo", "3d", "vector", "minimal", "surreal"
    ]
    
    # Process each image entry
    for entry in image_data:
        # Generate title from filename if missing
        if 'title' not in entry:
            filename = Path(entry['url']).stem if 'url' in entry else "untitled"
            # Clean up the filename to create a title
            title = filename.replace('-', ' ').replace('_', ' ').title()
            entry['title'] = title
        
        # Generate description if missing
        if 'desc' not in entry:
            entry['desc'] = f"Artwork titled: {entry.get('title', 'Untitled')}"
        
        # Generate tags if missing (try to extract from filename)
        if 'tags' not in entry:
            tags = set()
            filename = entry.get('url', '').lower()
            
            # Try to guess some tags from filename
            for tag in possible_tags:
                if tag in filename:
                    tags.add(tag)
            
            # Add some random tags if we didn't find any
            if not tags:
                tags.update(random.sample(possible_tags, min(3, len(possible_tags))))
            
            entry['tags'] = list(tags)
        
        # Generate date if missing (random date in last 2 years)
        if 'date' not in entry:
            random_days = random.randint(0, 730)  # 2 years
            random_date = datetime.now() - timedelta(days=random_days)
            entry['date'] = random_date.strftime('%Y-%m-%d')
        
        # Generate random likes and views if missing
        if 'likes' not in entry:
            entry['likes'] = random.randint(10, 500)
        
        if 'views' not in entry:
            entry['views'] = entry['likes'] * random.randint(2, 10)
    
    return image_data

def convert_json_file(input_path, output_path):
    """
    Convert JSON file from old format to new format
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        
        # Handle different possible old formats
        if isinstance(old_data, list):
            # Already an array of images
            new_data = old_data
        elif isinstance(old_data, dict):
            # Might be an object with images as properties
            new_data = list(old_data.values())
        else:
            raise ValueError("Unexpected JSON format")
        
        # Generate missing info
        new_data = generate_missing_info(new_data)
        
        # Save the new JSON file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2)
        
        print(f"Successfully converted JSON file. Output saved to {output_path}")
        return True
    
    except Exception as e:
        print(f"Error converting JSON file: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage
    input_json = "old_image_data.json"  # Your existing JSON file
    output_json = "new_image_data.json"  # Output file
    
    print("JSON Converter Tool")
    print("This will convert your old image JSON format to the new format with all required fields.")
    
    # Get input file path
    input_path = input("Enter path to your existing JSON file: ").strip() or input_json
    output_path = input("Enter path for the converted output file: ").strip() or output_json
    
    # Run the conversion
    success = convert_json_file(input_path, output_path)
    
    if success:
        print("\nConversion complete! Here's a sample of the converted data:")
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                sample_data = json.load(f)[:2]  # Show first 2 entries as sample
            print(json.dumps(sample_data, indent=2))
        except:
            print("(Could not display sample)")
    else:
        print("\nConversion failed. Please check your input file and try again.")