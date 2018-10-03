import time
import psutil
import subprocess
from threading import Thread

class WLInfo:
    def __init__(self, interface):
        self.interface = interface

    def removetrash(self, output):
        output = output.replace("\\t", "")
        output = output.replace("b", "", 1)
        output = output.replace("'", "")

        return output

    def encode_data(self, output):
        structure = output.split("\\n")

        devices = round(len(structure)/19)
        final = []
        for index in range(0,devices):
            device_info = {}
            station_mac = structure[index*19].split(" ")[1]
            
            data = structure[(index*19+1):((index+1)*19)]
            device_info["mac"] = station_mac
            
            for att in data:
                att_group = att.split(":")

                # Ajusting labels
                if att_group[0] == "TDLS peer":
                    att_group[0] = "tdls"
                elif att_group[0] == "MFP":
                    att_group[0] = "mfb"
                elif att_group[0] == "WMM/WME":
                    att_group[0] = "wmm"
                
                att_group[0] = att_group[0].replace(" ", "_")

                # Ajusting values
                if att_group[1] == "no":
                    att_group[1] = False
                elif att_group[1] == "yes":
                    att_group[1] = True
                
                device_info[att_group[0]] = att_group[1]

            final.append(device_info)

        return final

    def execute(self):
        try:
            output = str(subprocess.check_output(['iw', 'dev', self.interface, 'station', 'dump']))
            output = self.removetrash(output)

            encoded = self.encode_data(output)

            return encoded
        except:
            return []

class Throughput(Thread):
    def __init__(self, interface="enp3s0"):
        Thread.__init__(self)
        self.interface = interface
        self.exec_flag = True
        self.current_value = 0

    def run(self):
        old_value = 0;
        new_value = 0;
        while self.exec_flag:
            
            new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

            if old_value:
                self.current_value = self.send_stat(new_value - old_value)

            old_value = new_value

            time.sleep(1)

    def convert_to_mbit(self, value):
        return value/1024./1024.*8

    def send_stat(self, value):
        #print ("%0.3f" % self.convert_to_mbit(value))

        return self.convert_to_mbit(value)

    def get_value(self):
        return self.current_value
    
    def stop_thread(self):
        self.exec_flag = False