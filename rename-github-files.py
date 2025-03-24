import os
import subprocess

def rename_github_files():
    try:
        # First pass: Rename files with spaces
        for root, dirs, files in os.walk('images'):
            for file in files:
                if ' ' in file:
                    old_path = os.path.join(root, file)
                    new_name = file.replace(' ', '-')
                    new_path = os.path.join(root, new_name)
                    
                    subprocess.run(['git', 'mv', old_path, new_path])
                    print(f'Renamed: {old_path} → {new_path}')

        # Commit changes
        subprocess.run(['git', 'commit', '-m', 'chore: standardize filenames'])
        subprocess.run(['git', 'push'])
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    rename_github_files()