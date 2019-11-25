import sys
import os
import argparse
import json
import rosbag

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
    bag = rosbag.Bag(bagFile)
    if not bagFile.endswith(".bag"):
        raise NameError("Input file should be a .bag file")

    jsonFile = args.annotation
    if not jsonFile.endswith(".json"):
        raise NameError("Annotation file should be a .json file")

    return topic, start, end, bag, jsonFile

# prints out all available topics of the given bag file
def findTopics(bag):
    topics = bag.get_type_and_topic_info()[1].keys()
    types = []
    for i in range(0, len(bag.get_type_and_topic_info()[1].values())):
        types.append(bag.get_type_and_topic_info()[1].values()[i][0])
    print(types)

if __name__ == "__main__":
    set_topic, start_tag, end_tag, bag, jFile = initVars()
    
    findTopics(bag)

    bag.close()   