#!/usr/bin/env python3
import os
import json
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def get_image_metadata(image_path):
    """Extract basic metadata from an image file"""
    try:
        with Image.open(image_path) as img:
            # Get basic info
            info = {
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode,
            }
            
            # Try to get EXIF data if available
            exif_data = {}
            if hasattr(img, '_getexif') and img._getexif() is not None:
                for tag, value in img._getexif().items():
                    decoded = TAGS.get(tag, tag)
                    exif_data[decoded] = value
            
            # Extract creation date from EXIF if available
            create_date = None
            if 'DateTimeOriginal' in exif_data:
                create_date = exif_data['DateTimeOriginal']
            elif 'DateTime' in exif_data:
                create_date = exif_data['DateTime']
            
            return info, create_date
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None, None

def generate_image_list(folder_path, output_file='image-list.json'):
    """Generate JSON list of images with metadata"""
    # Supported image extensions
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
    
    # Prepare the image list
    image_list = []
    
    # Walk through the directory
    for root, _, files in os.walk(folder_path):
        for filename in files:
            # Skip non-image files
            if not filename.lower().endswith(valid_extensions):
                continue
                
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, start=folder_path)
            
            # Get image metadata
            metadata, create_date = get_image_metadata(full_path)
            if not metadata:
                continue
            
            # Prepare the image entry
            base_name = os.path.splitext(filename)[0]
            title = ' '.join([word.capitalize() for word in base_name.replace('_', ' ').replace('-', ' ').split()])
            
            image_entry = {
                'url': f"images/portfolio/{rel_path.replace(os.path.sep, '/')}",
                'alt': f"{title} image",
                'title': title,
                'desc': f"AI-generated artwork: {title}",
                'tags': ['digital', 'art'],  # Default tags, modify as needed
                'date': create_date or datetime.now().strftime('%Y-%m-%d'),
                'likes': 0,  # Default values
                'views': 0   # Default values
            }
            
            # Add some smart tagging based on filename
            if 'anubis' in filename.lower():
                image_entry['tags'].extend(['ai', 'mythology', 'egyptian'])
            elif 'pharaoh' in filename.lower():
                image_entry['tags'].extend(['ai', 'egyptian', 'animal'])
            elif 'cyber' in filename.lower():
                image_entry['tags'].extend(['digital', 'sci-fi', 'cityscape'])
            elif 'web' in filename.lower() or 'ui' in filename.lower():
                image_entry['tags'].extend(['web', 'design', 'ui'])
            
            # Remove duplicates from tags
            image_entry['tags'] = list(set(image_entry['tags']))
            
            image_list.append(image_entry)
    
    # Sort by date (newest first)
    image_list.sort(key=lambda x: x['date'], reverse=True)
    
    # Write to JSON file
    try:
        with open(output_file, 'w') as f:
            json.dump(image_list, f, indent=2)
        print(f"Successfully generated {output_file} with {len(image_list)} images.")
    except Exception as e:
        print(f"Error writing JSON file: {str(e)}")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate JSON list of images for portfolio website.')
    parser.add_argument('folder', help='Path to the folder containing images')
    parser.add_argument('--output', default='image-list.json', help='Output JSON filename')
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.folder):
        print(f"Error: {args.folder} is not a valid directory")
        exit(1)
    
    generate_image_list(args.folder, args.output)