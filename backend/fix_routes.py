import os
import re

def fix_response_models(directory):
    # Walk through all python files in the routes directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                # Read the file content
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Find and replace @router.get/post/put/delete patterns with response_model
                pattern = r'@router\.(get|post|put|delete|patch)\(.*?response_model\s*=\s*[^,\)]+.*?\)'
                # Replace with the same but without response_model parameter
                modified_content = re.sub(pattern, lambda m: re.sub(r',?\s*response_model\s*=\s*[^,\)]+', '', m.group(0)), content)
                
                # Write the modified content back if changed
                if content != modified_content:
                    with open(file_path, 'w') as f:
                        f.write(modified_content)
                    print(f"Modified: {file_path}")

if __name__ == "__main__":
    routes_dir = 'app/api/routes'
    fix_response_models(routes_dir)
    print("Done! All response_model parameters have been removed.")