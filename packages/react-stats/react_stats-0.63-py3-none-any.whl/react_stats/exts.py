

import os
import json


def exts_dict():
    
    cur_path = os.path.dirname(os.path.abspath(__file__))
    lang_path = os.path.join(cur_path, "languages.json")
    
    exts = {}
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



