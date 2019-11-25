#%%
import json
import os

def get_json_files(file_directory):
    json_files = []
    for f in file_directory:
        if  f.endswith(".json"):
            json_files.append(f)
    return json_files

def get_jsons(json_files):
    list_files = []
    for f in json_files:
        jfile = open(f, 'r')
        list_files.append(json.load(jfile))
    return list_files



def verify(jfile):
    instructions = ['start', 'reached', 'top', 'retract', 'rest']
    index = 0
    verified = True
    for k in jfile:
        entry = jfile[k]
        if entry["key"] == instructions[index]:
            index += 1
        else:
            #print("Error in " + jfile)
            verified = False
            
            print("error -> " + str(entry.get("rel_time_sec")))
            index = instructions.index(entry.get("key")) + 1
        if index > 4:
            index = 0
    
    return verified



if __name__ == "__main__":
    all_files = os.listdir()
    json_files = get_json_files(all_files) # list of json files (file names)
    jsons = get_jsons(json_files)  # list of jsons 
    for jfile in jsons:  # each json from list of jsons
        if  not verify(jfile):
            index = jsons.index(jfile)
            print("ERROR: " + json_files[index])

#%%