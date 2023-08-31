

import os
import json
import sys
import pkg_resources


def main():
    
    current_dir = os.getcwd()
    print("\n\nEnsure that you are in the root directory.")
    print(f"\ncurrently in: {current_dir}.")
    proceed = input(f"Do you want to proceee? (yes/no): ")
    
    if proceed.lower() != "yes":
        sys.exit("")
    else:
        make_structure(current_dir)
    
    
    
    
def make_structure(path):
    try: 
        os.makedirs(os.path.join(path, "assets"))

        resource_package = __name__
        resource_path = 'assets.json'
        assets_path = pkg_resources.resource_filename(resource_package, resource_path)
        
        with open(assets_path, "r") as file:
            file_types = json.load(file)["extension_to_folder"]
            dir_set = set(file_types.values())

            for dir in dir_set:
                os.makedirs(os.path.join(path, "assets", dir))
            
    except FileExistsError:
        sys.exit("Creation not possible. Assets dir already exists.")
    except Exception as e:
        sys.exit(f"An error occured: {e}")
    

if __name__ == "__main__":
    main()