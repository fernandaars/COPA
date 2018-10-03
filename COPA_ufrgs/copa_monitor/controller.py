import socket
import time
import json
import pprint
import requests
import sys

BASE_URL = "http://127.0.0.1:8000/REST/"

class Monitor():
    def __init__(self, name, host, port):
        self.host = host
        self.port = port
        self.name = name
        self.connected = False
        self.socket = None
        self.status = "not_connected"

    def getInfo(self):
        return {"name": self.name,"host": self.host, "port": self.port}

    def connect(self):
        try:
            if self.status == "not_connected":
                self.socket = socket.socket()
                self.socket.connect((self.host, self.port))
                self.connected = True
                self.status = "connected"
                return True
        except socket.error:
            self.connected = False
            return False

    def close(self):
        try:
            if self.connected:
                print("Disconnected from "+self.name)
                self.socket.close()
                self.status = "not_connected"
            return True
        except:
            return False

    def sendMessage(self, message):
        try:
            if self.connected:
                print(message["action"]+" sent to "+self.name)
                message = json.dumps(message)
                return self.socket.send(message.encode())
            else:
                return False
        except:
            self.connected = False
            self.status = "not_connected"
            print("Unexpected error sending message:", sys.exc_info()[0])
            return False

    def recvMessage(self):
        try:
            if self.connected:
                return json.loads(self.socket.recv(1024).decode())
            else:
                return False
        except:
            self.connected = False
            self.status = "not_connected"
            return False

    def register(self):
        if self.status == "connected":
            data = {
                "action": "register",
                "data": {"name": self.name}
            }
            
            if self.sendMessage(data):
                result = self.recvMessage()

                if result:
                    self.status = "wait_link"
                    return True

        return False

    def measureLinks(self, linkList):
        if self.status == "wait_link":
            data = {
                "action": "link_usage",
                "data": linkList
            }

            if self.sendMessage(data):
                result = self.recvMessage()

                if result:
                    self.status = "wait_init"
                    return True

        return False

    def initMonitor(self, target_list):
        if self.status == "wait_init":
            data = {
                "action": "init",
                "data": target_list
            }

            if self.sendMessage(data):
                result = self.recvMessage()

                if result:
                    self.status = "initiated"
                    return True

        return False

class Orchestrator():
    def __init__(self, monitorList):
        self.monitors = []

        for monitor in monitorList:
            self.monitors.append(Monitor(monitor["name"], monitor["host"],monitor["port"]))

    def addMonitorList(self, monitorList):
        for monitor in monitorList:
            self.monitors.append(Monitor(monitor["name"], monitor["host"],monitor["port"]))

    def connectMonitors(self):
        failed = []

        for monitor in self.monitors:
            if monitor.status == "not_connected":
                if not monitor.connect():
                    failed.append(monitor)
        
        return failed

    def registerMonitors(self):
        failed = []

        for monitor in self.monitors:
            if monitor.status == "connected":
                if not monitor.register():
                    failed.append(monitor)
        
        return failed

    def measureLinks(self):
        failed = []
        linkList = self.prepareLinks()
        
        for monitor in self.monitors:
            if monitor.status == "wait_link":
                if not monitor.measureLinks(linkList[monitor.host+":"+str(monitor.port)]):
                    failed.append(monitor)

        return failed

    def prepareLinks(self):
        links = {}
        pp = pprint.PrettyPrinter(indent=4)
        
        for i in range(0, len(self.monitors)):
            if self.monitors[i].status == "wait_link":
                #print("link: "+self.monitors[i].host+":"+str(self.monitors[i].port))
                links[self.monitors[i].host+":"+str(self.monitors[i].port)] = []
                for j in range(i+1, len(self.monitors)):
                    if self.monitors[j].status == "wait_link":
                        pp.pprint(links)
                        #print(self.monitors[j].host+":"+str(self.monitors[j].port))
                        links[self.monitors[i].host+":"+str(self.monitors[i].port)].append(self.monitors[j].getInfo())

        return links

    def initMonitors(self):
        failed = []

        for monitor in self.monitors:
            if monitor.status == "wait_init":
                if not monitor.initMonitor(self.getWaitInits(monitor.host, monitor.port)):
                    failed.append(monitor)

        return failed

    def closeConnections(self, closeType, monitorList):
        if closeType == "partial":
            for to_disconnect in monitorList:
                for key, monitor in enumerate(self.monitors):
                    if to_disconnect[1] == monitor.host:
                        if monitor.close():
                            monitor.connected = False
                            del self.monitors[key]
                            
        elif closeType == "all":
            for monitor in self.monitors:
                if monitor.close():
                    monitor.connected = False

        return True
    
    def getWaitInits(self, host, port):
        result = []

        for monitor in self.monitors:
            if (monitor.status == "wait_init" or monitor.status == "initiated") and (monitor.host != host or monitor.port != port):
                result.append(monitor.getInfo())

        return result
            
        

if __name__ == '__main__':
    monitorList = []
    old_monitorList = []
    orch = None

    data = {}
    # Get pools
    while True:
        try:
            monitors = requests.get(BASE_URL+"pools", data).json()

            # Format monitor list
            for monitor in monitors['pools']:
                exists = False;
                for key, old_monitor in enumerate(old_monitorList):
                    if monitor[1] == old_monitor[1]:
                        exists = True
                        del old_monitorList[key]
                        break;

                if not exists:
                    monitorList.append({
                        "name": monitor[0],
                        "host": monitor[1],
                        "port": 5000
                    })

            # Initiate orchestrator
            if orch == None:
                # print("Init orch!")
                orch = Orchestrator(monitorList)
            elif monitorList != []:
                # print("Add monitor list")
                orch.addMonitorList(monitorList)
                orch.closeConnections("all", [])

            # print("From monitorList:")
            # for monitor in monitorList:
            #     print(monitor["name"]+" - "+monitor["host"])

            # print("From orch:")
            # for monitor in orch.monitors:
            #     print(monitor.name+" - "+monitor.status)

            # print("From old_list:")
            # for monitor in old_monitorList:
            #     print(monitor[0]+" - "+monitor[1])

            if old_monitorList != []:
                orch.closeConnections("partial", old_monitorList)
                orch.closeConnections("all", [])

            orch.connectMonitors()
            orch.registerMonitors()
            orch.measureLinks()
            orch.initMonitors()
            old_monitorList = monitors['pools']
            monitorList = []
            time.sleep(5)
        except KeyboardInterrupt:
            orch.closeConnections("all",[])
            break;
        except:
            print("Unexpected error sending message:", sys.exc_info())
            orch.closeConnections("all",[])
            orch = None
            monitorList = []
        