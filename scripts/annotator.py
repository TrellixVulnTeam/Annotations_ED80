import sys
import os
import argparse
import json, yaml
import rosbag, rospy


### https://github.com/uos/rospy_message_converter ###
from rospy_message_converter import message_converter 
from std_msgs.msg import String
import genpy

from collections import OrderedDict as ODict

path = os.getcwd()
json_path = path + "/jsons"

text = """This program will create multiple .txt files of the ROS messages that are in the input .bag file. It chooses which messages 
    to  record by using the given annotation .json file and creating time frames between the two input 
    annotation tags. Each different created file is a different timeframe.""" 

parser = argparse.ArgumentParser(description = text)
required = parser.add_argument_group("required file arguments")
required.add_argument("--topic", "-t", help="set topic to record", required=True)
required.add_argument("--start", "-s", help="set start tag", required=True)
required.add_argument("--end", "-e", help="set end tag", required=True)
required.add_argument("--input", "-i", help="set the input bag file", required=True)
required.add_argument("--annotation", "-a", help="set the annotation file", required=True)
required.add_argument("--output", "-o", help="set the output json file", required=True)
args = parser.parse_args()

def initVars():
    # set the values from the arguments
    topic = str(args.topic)
    start = args.start
    end = args.end
     
    bagFile = str(args.input)
    if not bagFile.endswith(".bag"):
        raise NameError("Input file should be a .bag file")
    bag = rosbag.Bag(bagFile, 'r')


    f = args.annotation
    if not f.endswith(".json"):
        raise NameError("Annotation file should be a .json file")
    f_path = json_path + "/" + f
    jsonFile = open(f_path, 'r')
    jDict = json.load(jsonFile)

    outFile = args.output
    if not outFile.endswith(".json"):
        outFile = outFile + ".json"
    output = open(outFile, 'w')
    

    return topic, start, end, bag, jDict, output

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
            time = genpy.Time(entry["timestamp"]["secs"], entry["timestamp"]["nsecs"])
            start_times.append(time) 
        if entry["key"] == end:
            time = genpy.Time(entry["timestamp"]["secs"], entry["timestamp"]["nsecs"])
            end_times.append(time)
    
    return [start_times, end_times]

# sends each key to the appropriate file
def send_to_files(start_times, end_times, full_dict, filename):
    # create subdirectory for all the output files
    sub_dir = filename + "_messages/"
    try:
        os.mkdir(sub_dir, 0o777)
    except OSError as err:
        print(err)

    for entry in full_dict:
       #print("entry in ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        msg = full_dict[entry]
        msg_time = [msg["timestamp"]["secs"], msg["timestamp"]["nsecs"]]
        for start, end in zip(start_times, end_times):
            #print(start.secs, "AND", end.secs)
            #print(msg_time)
            if time_lessthan(msg_time, end) and time_greaterthan(msg_time, start):
                #print("IN TIME")
                index = start_times.index(start)
                name = filename + str(index) + ".txt"
                print(name)
                sectioned_file = open(sub_dir + name, "a+")
                sectioned_file.write(str(msg["msg"]))
                sectioned_file.close()
                pass



# compares time1 and time2
# returns time1 < time2
def time_lessthan(time1, time2):
    time1_sec = time1[0]
    time1_nsec = time1[1]
    time2_sec = time2.secs
    time2_nsec = time2.nsecs

    if time1_sec != time2_sec:
        return time1_sec < time2_sec
    elif time1_nsec != time2_nsec:
        return time1_nsec < time2_nsec
    else:
        return True

# compares time1 and time2
# returns time1 > time2
def time_greaterthan(time1, time2):
    time1_sec = time1[0]
    time1_nsec = time1[1]
    time2_sec = time2.secs
    time2_nsec = time2.nsecs

    if time1_sec != time2_sec:
        return time1_sec > time2_sec
    elif time1_nsec != time2_nsec:
        return time1_nsec > time2_nsec
    else:
        return True

if __name__ == "__main__":
    set_topic, start_tag, end_tag, bag, json_dict, output = initVars()
    

    [start_times, end_times] = find_times(start_tag, end_tag, json_dict)

    # print("HERE >>> topic={}, start={}, end={}".format(set_topic, start, end))
    # print(set_topic)
    # print(type(set_topic))

    # empty ordered dictionary stolen from annotator widget
    output_dict = ODict()
    index = 0

    # go through all specified messages
    for msg_topic, msg, t in bag.read_messages(topics = set_topic):

        # convert message with ros converter
        full_message = message_converter.convert_ros_message_to_dictionary(msg)

        # create new dict for json entries
        output_dict[index] = {"timestamp": {"secs": t.secs, 
                                  "nsecs": t.nsecs},
                            "msg": full_message}

        # printing for visualization
        print(full_message)

        # increase index of the json keys
        index += 1
    
    # dump dictionary to json
    json.dump(output_dict, output, sort_keys=True, indent=3)
    # create copied output file name
    filename = str(output.name)[:-5]
    # send messages to appropriate files
    send_to_files(start_times, end_times, output_dict, filename)
    
    output.close()
    bag.close()   