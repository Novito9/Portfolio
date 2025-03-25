import json
from pathlib import Path

# Path to your JSON file
json_file = Path(r"C:\Users\9\Documents\Novito9\Portfolio\images\image-list.json")

# Read the file content
with open(json_file, "r", encoding="utf-8") as f:
    content = f.read()

# Function to extract valid JSON objects
def extract_valid_json(content):
    valid_objects = []
    stack = []
    start_index = 0

    for i, char in enumerate(content):
        if char == "{":
            stack.append(i)
        elif char == "}":
            if stack:
                start_index = stack.pop()
                if not stack:  # If the stack is empty, we have a complete object
                    try:
                        obj = json.loads(content[start_index:i+1])
                        valid_objects.append(obj)
                    except json.JSONDecodeError:
                        continue  # Skip invalid objects
    return valid_objects

# Extract valid JSON objects
valid_objects = extract_valid_json(content)

# Save the valid JSON objects to a new file
output_file = Path(r"C:\Users\9\Documents\Novito9\Portfolio\images\image-list-clean.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(valid_objects, f, indent=2)

print(f"Extracted {len(valid_objects)} valid JSON objects. Saved to {output_file}")