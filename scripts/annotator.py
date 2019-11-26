import sys
import os
import argparse
import json, yaml
import rosbag, rospy


### https://github.com/uos/rospy_message_converter ###
from rospy_message_converter import message_converter 
from std_msgs.msg import String
import genpy

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
            start_times.append(time) # append k b/c k is the rostime 
        if entry["key"] == end:
            time = genpy.Time(entry["timestamp"]["secs"], entry["timestamp"]["nsecs"])
            end_times.append(time)
    
    return [start_times, end_times]


# writes the messages to their separate output files
def write_to_seperate_files(start_times, end_times, outputJSON):
    for l in outputJSON:
        #l = l[:-1]
        send_to_file(start_times, end_times, l, outputJSON.name)

# sends each line to the appropriate file
def send_to_file(start_times, end_times, message, filename):
    message_time = [message["timestamp"]["secs"], message["timestamp"]["nsecs"]]

    for start, end in zip(start_times, end_times):
        if time_lessthan(message_time, end) and time_greaterthan(message_time, start):
            index = start_times.index(start)
            filename = str(index) + ".txt"
            print(filename)
            sectioned_file = open(filename, "a+")
            sectioned_file.write(message)
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
    '''
        for start, end in zip(start_times, end_times):
            bag = rosbag.Bag('thebag.bag')
            # print(bag)
    '''
    # print("HERE >>> topic={}, start={}, end={}".format(set_topic, start, end))
    # print(set_topic)
    # print(type(set_topic))

    for msg_topic, msg, t in bag.read_messages(topics = set_topic):
        # msg = String(data = "Help")
        # if msg_topic == set_topic:

        full_message = message_converter.convert_ros_message_to_dictionary(msg)
        dict_out = {"timestamp": {"secs": t.secs, 
                                  "nsecs": t.nsecs},
                    "msg": full_message}
        print(full_message)
        send_to_file(start_times, end_times, dict_out, output.name)

        json_dict = json.dumps(dict_out)
        output.write(json_dict)
        output.write("\n")

    name = output.name
    output.close()

    bag.close()   