#Throughput and Loopthread
from pprint import pprint
from threading import Thread
import time
import psutil

#LXD
import os.path

# Owping, Iperf3 and wlinfo
import subprocess

class Owping:
    def __init__(self, container, targetip):
        self.container = container
        self.targetip = targetip

    def removetrash(self, output):
        output = output.replace("(", "")
        output = output.replace(")", "")
        output = output.replace("'", "")
        output = output.replace("b", "", 1)

        return output

    def encode_jitter(self, structure):
        jitter_structure = structure[1].split("=")[1]
        onewayjitter = {}
        onewayjitter['value'] = jitter_structure.split(" ")[1]
        onewayjitter['unit'] = jitter_structure.split(" ")[2]

        return onewayjitter

    def encode_latency(self, structure):
        ping_structure = structure[0].split(" ")
        ping_structure = ping_structure[4].split("/")

        onewayping = {}
        onewayping['min'] = ping_structure[0]
        onewayping['median'] = ping_structure[1]
        onewayping['max'] = ping_structure[2]

        return onewayping

    def encode_data(self, output):
        upload_structure = output.split("\\n")[7:9]
        encoded = {}

        latency = self.encode_latency(upload_structure)
        encoded["latency_max_1to2"] = latency["max"]
        encoded["latency_median_1to2"] = latency["median"]
        encoded["latency_min_1to2"] = latency["min"]
        encoded["jitter_1to2"] = self.encode_jitter(upload_structure)["value"]

        download_structure = output.split("\\n")[18:20]
        latency = self.encode_latency(download_structure)

        encoded["latency_max_2to1"] = latency["max"]
        encoded["latency_median_2to1"] = latency["median"]
        encoded["latency_min_2to1"] = latency["min"]
        encoded["jitter_2to1"] = self.encode_jitter(download_structure)["value"]

        median = (float(encoded["latency_median_1to2"]) + float(encoded["latency_median_2to1"]))/2
        if median < 0:
            median = 0.1

        median = str(round(median, 2))

        encoded["latency_median_1to2"] = median
        encoded["latency_median_2to1"] = median

        return encoded

    def get_targetip(self):
        return self.targetip

    def execute(self):
        try:
            if self.container != None:
                output = str(subprocess.check_output(['lxc', 'exec', self.container, '--', 'owping', self.targetip]))
            else:
                output = str(subprocess.check_output(['owping', self.targetip]))
            #print(output) 
            output = self.removetrash(output)
            encoded = self.encode_data(output)

            return encoded
        except:
            print("Owping execution could not end.")
            raise

class Iperf3:
    def __init__(self, container, targetip, port=5001):
        self.container = container
        self.targetip = targetip
        self.port = port

    def removetrash(self, output):
        output = output.replace("(", "")
        output = output.replace(")", "")
        output = output.replace("'", "")
        output = output.replace("b", "", 1)

        return output

    def encode_data(self, output):
        structure = output.split("\\n")
        data = structure[15:-3]

        upload = {}
        upload['value'] = data[0].split(" ")[12]
        upload['unit'] = data[0].split(" ")[13]

        download = {}
        download['value'] = data[1].split(" ")[12]
        download['unit'] = data[1].split(" ")[13]

        encoded = {}
        encoded['upload'] = upload
        encoded['download'] = download

        return encoded

    def execute(self):
        if self.container != None:
            output = str(subprocess.check_output(['lxc', 'exec', self.container, '--', 'iperf3', '-c', self.targetip, '-p', str(self.port)]))
        else:
            output = str(subprocess.check_output(['iperf3', '-c', self.targetip, '-p', str(self.port)]))

        output = self.removetrash(output)
        encoded = self.encode_data(output)

        return encoded

