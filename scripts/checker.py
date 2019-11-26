import json
import os
import sys

path = os.getcwd()
json_path = path + "/jsons"

# takes in a list of file names and returns a list
# of only json files
def get_json_files(file_directory):
    json_files = []
    for f in file_directory:
        if  f.endswith(".json"):
            json_files.append(f)
    return json_files


# takes in a list of json files and returns a list
# of jsons (dictionaries)
def get_jsons(json_files):
    list_jsons = []
    for f in json_files:
        f = json_path + "/" + f
        jfile = open(f, 'r')
        list_jsons.append(json.load(jfile))
    return list_jsons

# verifies the order of tags in the input json
def verify(json_dict):
    instructions = ['start', 'reached', 'top', 'retract', 'rest']
    index = 0
    verified = True

    
    keys = sorted(list(json_dict.keys()))
    for k in keys:
        entry = json_dict[k]
        if entry["key"] == instructions[index]:
            index += 1
        else:
            #print("Error in " + json_dict)
            verified = False
            
            err = "error -> " + str(entry.get("rel_time_sec"))
            err = err + "\tread %s when the next command should be %s (prev is %s)" % (entry["key"], instructions[index], instructions[index -1])
            print(err)
            index = instructions.index(entry.get("key")) + 1
        if index > 4:
            index = 0
    
    return verified



if __name__ == "__main__":
    all_files = os.listdir(json_path)
    json_files = get_json_files(all_files) # list of json files (file names)
    jsons = get_jsons(json_files)  # list of jsons 
    for json_dict in jsons:  # each json from list of jsons
        if not verify(json_dict):
            index = jsons.index(json_dict)
            print("ERROR: " + json_files[index])