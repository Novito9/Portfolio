import os
import subprocess

def rename_git_files(folder):
    for root, dirs, files in os.walk(folder):
        for name in files:
            if ' ' in name:
                old_path = os.path.join(root, name)
                new_name = name.replace(' ', '-')
                new_path = os.path.join(root, new_name)
                
                # Use git mv to preserve history
                subprocess.run(['git', 'mv', old_path, new_path])
                print(f'Renamed: {name} → {new_name}')

# Update these paths
rename_git_files('images')
rename_git_files('other-folder')