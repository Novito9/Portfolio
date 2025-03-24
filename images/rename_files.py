import os
import shutil

folder_path = 'path/to/your/images'
for filename in os.listdir(folder_path):
    if ' ' in filename:
        new_name = filename.replace(' ', '-')
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_name)
        shutil.move(src, dst)