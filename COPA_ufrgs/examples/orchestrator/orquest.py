# Move a video server to the location where most clients are based at
# !/usr/bin/env python3

# from pylxd import exceptions, Client
import time
from collections import defaultdict

import matplotlib.pyplot as plt

# from plotter import *
# from apirequester import *

# Number of samples to be considered for migration decision
# (less = more aggressive; < 5 NOT recommended)
SAMPLE_SIZE = 5

# Threshold between clients' traffic that triggers migration
DIFF_THRESHOLD = 0.8
# Interval between two orchestration loop cycles
ORCHESTRATION_INTERVAL = 5

i = 0
videoLocation = "Server2"
locationComplement = "Server1"
containerPools = {"Server1": "Clients", "Server2": "Clients"}
videoServer = "Cavalo"
dataPrevious = {}
dataCurrent = {}
dataAvg = {}
cyclesCompleted = 1


# Aux function to automatically add keys to a dict when they don't already exist
def recursively_default_dict():
    return defaultdict(recursively_default_dict)


# update_traffic_delta:
# For container in container_pool, calculates difference between current and
# previous measures for packets in and out; updates  measurements/lists
# accordingly
def update_traffic_delta(container_pool, container):
    global dataPrevious
    global dataCurrent
    global dataAvg
    delta_in = (float(dataCurrent[container_pool][container]["in"])
                - float(dataPrevious[container_pool][container]["in"]))
    delta_out = (float(dataCurrent[container_pool][container]["out"])
                 - float(dataPrevious[container_pool][container]["out"]))
    dataPrevious[container_pool][container]["in"] = \
        dataCurrent[container_pool][container]["in"]
    dataPrevious[container_pool][container]["out"] = \
        dataCurrent[container_pool][container]["out"]

    dataAvg[container_pool][container]["in"].append(delta_in)
    dataAvg[container_pool][container]["out"].append(delta_out)
    if len(dataAvg[container_pool][container]["in"]) > SAMPLE_SIZE:
        dataAvg[container_pool][container]["in"].pop(0)
        dataAvg[container_pool][container]["out"].pop(0)


# get_traffic_avg:
# For container in container_pool, return average for packets in and out
def get_traffic_avg(container_pool, container):
    global dataAvg
    avg_in_list = dataAvg[container_pool][container]["in"]
    avg_out_list = dataAvg[container_pool][container]["out"]
    avg_in = 0
    avg_out = 0
    for i in avg_in_list:
        avg_in += i
    for i in avg_out_list:
        avg_out += i
    avg_in = avg_in / len(avg_in_list)
    avg_out = avg_out / len(avg_out_list)
    return avg_in, avg_out


# get_pkts_counters:
# Returns in and out packet counters from container, retrieved from COPA API;
# assumes eth0 (maybe change that?)
def get_pkts_counters(container_pool, container):
    network_info = req_api(container_pool, container, "information")

    # print(network_info)

    pktIn = network_info['result']['network']['eth0']['counters'][
        'packets_received']
    pktOut = network_info['result']['network']['eth0']['counters'][
        'packets_sent']

    return pktIn, pktOut


# set_initial_values:
# Initialize dataPrevious for container in container_pool with initial values
# (the counter retrieved from when this function is called)
def set_initial_values(container_pool, container):
    global dataPrevious
    global dataCurrent
    global dataAvg

    dataPrevious[container_pool][container]["in"], \
    dataPrevious[container_pool][container]["out"] = get_pkts_counters(
            container_pool, container)
    dataCurrent[container_pool][container]["in"], \
    dataCurrent[container_pool][container]["out"] = {}, {}
    dataAvg[container_pool][container]["in"], \
    dataAvg[container_pool][container]["out"] = [], []


# Initializes data, filling previous data with initial counter
def init_data():
    global dataPrevious
    global dataCurrent
    global dataAvg
    global cyclesCompleted

    dataPrevious = {}
    dataCurrent = {}
    dataAvg = {}
    # We need to auto-create keys to the dict when needed
    dataPrevious = recursively_default_dict()
    dataCurrent = recursively_default_dict()
    dataAvg = recursively_default_dict()

    cyclesCompleted = 1

    # TODO: replace hardcoded initialization for hardcoded containers with a
    # better container mapping
    set_initial_values(videoLocation, videoServer)

    for pool, container in containerPools.items():
        set_initial_values(pool, container)


# Updates current values for in and out counters for all containers
def update_current_values():
    global dataCurrent
    global dataPrevious

    dataCurrent[videoLocation][videoServer]["in"], \
    dataCurrent[videoLocation][videoServer]["out"] = get_pkts_counters(
            videoLocation, videoServer)

    for pool, container in containerPools.items():
        dataCurrent[pool][container]["in"], dataCurrent[pool][container][
            "out"] = get_pkts_counters(pool, container)


# Aux function to make the API call to migrate the container, then swapping the
# variables for the server's location
def migrate(container, orig, dest):
    global videoLocation
    global locationComplement
    a = req_api(orig, container, "migrate", {"destination_pool": dest})
    videoLocation, locationComplement = locationComplement, videoLocation
    return a


init_data()
start = time.time()

plt.ion()
plt.ylabel('Traffic (Packets/s)')
plt.xlabel('Time (s)')
prevTime = start
prevValue = 0
currentComp = 0

while 1:
    update_current_values()
    update_traffic_delta(videoLocation, videoServer)

    for pool, container in containerPools.items():
        update_traffic_delta(pool, container)

    current_server_in, current_server_out = get_traffic_avg(videoLocation,
                                                            videoServer)
    current_nearest_in, current_nearest_out = get_traffic_avg(videoLocation,
                                                              "Clients")
    currentComp = current_nearest_in / (current_server_out + 0.000001)

    if len(dataAvg[videoLocation][videoServer]["in"]) >= SAMPLE_SIZE:
        # print("Conta {}! Considerado {}".format(current_nearest_in /
        #                                         (current_server_out
        #                                          + 0.00000001),
        #                                         DIFF_THRESHOLD
        #                                         / (1 + DIFF_THRESHOLD)))
        # Case nearest Clients are consuming at least DIFF_THRESHOLD times what
        #  afar clients are
        # if (current_nearest_in / (current_server_out + 0.00000001)
        #     > DIFF_THRESHOLD / (1 + DIFF_THRESHOLD)):
        if (float(current_nearest_in) / float(current_server_out + 0.00000001)
                > 1.0 - DIFF_THRESHOLD or current_server_out < 50):
            print("Orchestrator: Client near in {}  {} {} Nothing to do! Cycle "
                  "#{} Completed".format(current_nearest_in,
                                         current_server_out,
                                         current_nearest_in
                                         / (current_server_out + 0.00000001),
                                         cyclesCompleted))

        else:
            print("Orchestrator: Threshold has been reached! Migrating Video "
                  "Server from {} to {}".format(videoLocation,
                                                locationComplement))
            # continue
            res = migrate(videoServer, videoLocation, locationComplement)
            if int(res['code']) != 0:
                print("Orchestrator: Migration failed!"
                      "Error: {}".format(res["message"]))
                continue
            else:
                # Restart measures after migration
                set_initial_values(videoLocation, videoServer)
                for pool, container in containerPools.items():
                    set_initial_values(pool, container)
                print("Orchestrator: Video Server container migrated!"
                      " Cycle #{} Completed".format(cyclesCompleted))

    else:
        print("Orchestrator: Insufficient data for meaningful answer!"
              " (Cycle {}/{})".format(
                len(dataAvg[videoLocation][videoServer]["in"]), SAMPLE_SIZE))

    cyclesCompleted += 1

    plt.plot([prevTime, time.time() - start],
             [prevValue, currentComp],
             label='Values', color='b')
    plt.plot([prevTime, time.time() - start],
             [1.0 - DIFF_THRESHOLD,
              1.0 - DIFF_THRESHOLD],
             label='Threshold', color='r')
    # plt.legend([line_current, line_current], ['Efficiency','Threshold'])
    plt.pause(0.05)
    # print(prevValue, currentComp)
    prevTime = time.time() - start
    prevValue = currentComp

    # print(dataPrevious[videoLocation][videoServer]["out"])
    time.sleep(ORCHESTRATION_INTERVAL)
