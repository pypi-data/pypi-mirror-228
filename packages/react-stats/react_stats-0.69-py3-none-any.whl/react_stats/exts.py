import os
import json
import pkg_resources

def exts_dict():
    
    resource_package = __name__
    resource_path = '/'.join(('languages.json',))  # Do not use os.path.join() here; this is the package path
    lang_path = pkg_resources.resource_filename(resource_package, resource_path)

    exts = {}
    print(f"Looking for languages.json in: {lang_path}")
    with open(lang_path, "r") as file:
        data = json.load(file)
        
        for language in data:
            try:
                if len(language['extensions']) == 1:
                    exts[language['extensions'][0]] = language['name']
                elif len(language['extensions']) > 1:
                    for ext in language['extensions']:
                        exts[ext] = language['name']
            except KeyError:
                continue
    return exts
