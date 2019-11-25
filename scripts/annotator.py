import sys
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

if __name__ == "__main__":
    # set the values from the arguments
    topic = args.topic
    start_tag = args.start
    end_tag = args.end
    bagFile = str(args.input)
    bag = rosbag.Bag(bagFile)
    print(bagFile)
    if not bagFile.endswith(".bag"):
        Exception: "Input file should be a .bag file"
    jsonFile = args.annotation
    print(jsonFile)

    

