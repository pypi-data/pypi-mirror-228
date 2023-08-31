

import os
import json
import sys



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
        os.makedirs("assets")
        
        os.chdir(path + "/assets")

        with open(path + "/assets.json", "r") as file:
            file_types = json.load(file)["extension_to_folder"]
            dir_set = set(file_types.values())

            for dir in dir_set:
                os.makedirs(dir)
            
    except FileExistsError:
        sys.exit("Creation not possible. Assets dir already exists.")
    
    

if __name__ == "__main__":
    main()