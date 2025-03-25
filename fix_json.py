import json
import re
from pathlib import Path

# Path to your JSON file
json_file = Path(r"C:\Users\9\Documents\Novito9\Portfolio\images\image-list.json")

# Read the file content
with open(json_file, "r", encoding="utf-8") as f:
    content = f.read()

# Fix common JSON issues
try:
    # Attempt to load the JSON
    data = json.loads(content)
    print("JSON is valid.")
except json.JSONDecodeError as e:
    print(f"JSON is invalid. Attempting to fix... Error: {e}")
    # Remove invalid PowerShell code
    content = re.sub(r"\]\.Name\)`.*?\"", "", content, flags=re.DOTALL)
    # Remove trailing commas
    content = re.sub(r",\s*}", "}", content)
    content = re.sub(r",\s*]", "]", content)
    # Attempt to load the fixed JSON
    try:
        data = json.loads(content)
        print("JSON fixed successfully.")
    except json.JSONDecodeError as e:
        print(f"Failed to fix JSON. Error: {e}")
        exit(1)

# Save the fixed JSON
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("JSON file updated successfully.")