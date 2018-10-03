import requests
from pprint import pprint

class ExperimentServer:
    def __init__(self, addr):
        self.rooturl = "http://"+addr+":8000/REST/network"

    def send(self, url, data):
        r = requests.post(url, data)

        if r.status_code == 200:
            pprint(data)
            pprint(r.json())
        else:
            print("Error: ", r.status_code)

    def send_kpilink(self, data):
        self.send(self.rooturl+"/kpilink/", data)

        return True

    def send_kpiwireless(self, data):
        url = self.rooturl+"/kpiwireless/"
        r = requests.post(url, json=data)

        if r.status_code == 200:
            pprint(data)
            pprint(r.json())
        else:
            print("Error: ", r.status_code)

        return True

    def send_kpiresource(self, data):
        self.send(self.rooturl+"/kpiresource/", data)

        return True

    def register_tier(self, ip):
        return True