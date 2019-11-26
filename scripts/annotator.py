import sys
import os
import argparse
import json
import rosbag

path = os.getcwd()
json_path = path + "/jsons"

text = 'This is a test program. It demonstrates how to use the argparse module with a program description.'

parser = argparse.ArgumentParser(description = text)
required = parser.add_argument_group("required file arguments")
required.add_argument("--topic", "-t", help="set topic to record", required=True)
required.add_argument("--start", "-s", help="set start tag", required=True)
required.add_argument("--end", "-e", help="set end tag", required=True)
required.add_argument("--input", "-i", help="set the input bag file", required=True)
required.add_argument("--annotation", "-a", help="set the annotation file", required=True)
args = parser.parse_args()

def initVars():
    # set the values from the arguments
    topic = args.topic
    start = args.start
    end = args.end
     
    bagFile = str(args.input)
    if not bagFile.endswith(".bag"):
        raise NameError("Input file should be a .bag file")
    bag = "bag"#rosbag.Bag(bagFile)


    f = args.annotation
    if not f.endswith(".json"):
        raise NameError("Annotation file should be a .json file")
    f_path = json_path + "/" + f
    jsonFile = open(f_path, 'r')
    jDict = json.load(jsonFile)

    return topic, start, end, bag, jDict

# prints out all available topics of the given bag file
def findTopics(bag):
    topics = bag.get_type_and_topic_info()[1].keys()
    types = []
    for i in range(0, len(bag.get_type_and_topic_info()[1].values())):
        types.append(bag.get_type_and_topic_info()[1].values()[i][0])
    print(types)

# returns lists of the times of starts and ends
def find_times(start, end, json_dict):
    start_times = []
    end_times = []
    keys = sorted(list(json_dict.keys()))
    for k in keys:
        entry = json_dict[k]
        if entry["key"] == start:
            start_times.append(entry.get("rel_time_sec"))
        if entry["key"] == end:
            end_times.append(entry.get("rel_time_sec"))
    
    return [start_times, end_times]


if __name__ == "__main__":
    set_topic, start_tag, end_tag, bag, json_dict = initVars()
    
    #findTopics(bag)
    [start_times, end_times] = find_times(start_tag, end_tag, json_dict)
    




    bag.close()   