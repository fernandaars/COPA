import time
import psutil
from threading import Thread
from passive_monitoring import Throughput, WLInfo
from datasave import ExperimentServer
from active_monitoring import Iperf3, Owping
import requests
from pprint import pprint

my_interface = "br0"
wireless_interface = "ap0"

class StateMachine():
    def __init__(self):
        self.state = "not_connected"
        self.conditions = {
            "wait_register": {"register": self.register},
            "wait_link": {"link_usage": self.use_link},
            "wait_init": {"init": self.init_monitoring}
        }
        self.container = None
        self.wiface = wireless_interface
        self.server = ExperimentServer("qualquer coisa")
        self.loopthread = None
        self.name = ""

    def do_action(self, action, data):
        if self.state  in self.conditions:
            if action in self.conditions[self.state]:
                print("Executing action {}".format(action))
                return self.conditions[self.state][action](data)
        return {
            "status": "error"
        }

    def set_experimentserver(self, addr):
        self.server = ExperimentServer(addr)

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_name(self, name):
        self.name = name

    def register(self, data):
        self.set_state("wait_link")

        self.set_name(data["name"])
        if self.loopthread != None:
            self.loopthread.stop_thread()
            self.loopthread.join()
            self.loopthread = None

        return {
            "status": "wait_link"
        }

    def use_link(self, links=[]):
        self.set_state("active_measuring")

        for link in links:
            iperf3 = Iperf3(self.container, link["host"], 5001)
            #self.server.send_status(iperf3.execute())

        self.set_state("wait_init")
        return {
            "status": "wait_init"
        }

    def init_monitoring(self, data):
        self.set_state("init")
        #init Loopthread here
        if self.loopthread == None:
            if self.wiface:
                iwinfo = WLInfo(self.wiface)
            else:
                iwinfo = None
            self.loopthread = LoopThread(self.name, self.server, self.container, iwinfo, data)

            self.loopthread.start()
            self.initiated = True

        return {
            "status": "initiated"
        }

class LoopThread(Thread):
    """ Responsible for sending Latency measurements to the CoLiSEU monitor.
    """
    def __init__(self, name, server, container, iwinfo, target_list):
        Thread.__init__(self)
        self.exec_flag = True
        self.container = container
        self.target_list = target_list
        self.iwinfo = iwinfo
        self.status = {}
        self.name = name
        self.server = server
        self.throughput = Throughput(my_interface)

    def run(self):
        self.throughput.start()
        size = len(self.target_list)
        index = 0

        while self.exec_flag:
            try:
                link = {}
                wireless = []
                resource = {}
                if size != 0:
                    owping = Owping(self.container, self.target_list[index]["host"])
                    link = owping.execute()
                    link["locus1"] = self.name
                    link["locus2"] = self.target_list[index]["name"]
                    link['throughput'] = self.throughput.get_value()

                    index = (index + 1) % size

                if self.iwinfo:
                    wireless = self.iwinfo.execute()
                else:
                    wireless = []

                resource['locus'] = self.name
                resource['CPU'] = psutil.cpu_percent(interval=None)
                resource['memory'] = psutil.virtual_memory().percent

                self.server.send_kpilink(link)
 
                if wireless != []:
                    for id_wless, device in enumerate(wireless):
                        wireless[id_wless]['locus'] = self.name

                    self.server.send_kpiwireless(wireless)

                self.server.send_kpiresource(resource)

                time.sleep(1)
            except:
                print("Something gone wrong at Loop thread.")
                raise

    def stop_thread(self):
        self.exec_flag = False
        self.throughput.stop_thread()
        self.throughput.join()