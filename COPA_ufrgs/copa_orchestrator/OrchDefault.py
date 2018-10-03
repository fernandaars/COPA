#
#   Model class for orquestration algorithms
#

from core.models import Container, Pool
from monitor.models import KPIResources, KPILink, KPIWireless
from datetime import datetime, timedelta

class OrchDefault():
    def __init__():
        # Interval of data from servers (Minutes):
        # Example: Data from last 2 minutes
        self.time_interval = 2

    def setTimeInterval(self, interval):
        self.time_interval = interval

    def getTimeInterval(self):
        return self.time_interval

    def getServers(self):
        return list(Pool.objects.all().values())
    
    def getContainers(self, server):
        return list(Container.objects.get(pool=server).values())

    def getResources(self, server):
        time_threshold = datetime.now() - timedelta(minutes=self.getTimeInterval)
        
        return list(KPIResources.objects.get(pool=server, timestamp__gt=time_threshold).values())

    def getLinks(self, server):
        temp = dict()
        time_threshold = datetime.now() - timedelta(minutes=self.getTimeInterval)
        
        data = list(
                KPILink.objects.filter((Q(locus1=server) | Q(locus2=server)), timestamp__gt=time_threshold)
                .order_by("-timestamp")
                .values())

        for item in data:
            if item["locus1_id"] == locus.name:
                if not (item["locus2_id"] in temp):
                    temp[item["locus2_id"]] = {
                        "name": item["locus2_id"],
                        "jitter_down": [item["jitter_2to1"]],
                        "jitter_up": [item["jitter_1to2"]],
                        "latency_down": [item["latency_median_2to1"]],
                        "latency_up": [item["latency_median_1to2"]]
                    }
                else:
                    temp[item["locus2_id"]]["jitter_down"].insert(0, item["jitter_2to1"])
                    temp[item["locus2_id"]]["jitter_up"].insert(0, item["jitter_1to2"])
                    temp[item["locus2_id"]]["latency_down"].insert(0, item["latency_median_2to1"])
                    temp[item["locus2_id"]]["latency_up"].insert(0, item["latency_median_1to2"])
            else:
                if not (item["locus1_id"] in temp):
                    temp[item["locus1_id"]] = {
                        "name": item["locus1_id"],
                        "jitter_down": [item["jitter_1to2"]],
                        "jitter_up": [item["jitter_2to1"]],
                        "latency_down": [item["latency_median_1to2"]],
                        "latency_up": [item["latency_median_2to1"]]
                    }
                else:
                    temp[item["locus1_id"]]["jitter_down"].insert(0, item["jitter_1to2"])
                    temp[item["locus1_id"]]["jitter_up"].insert(0, item["jitter_2to1"])
                    temp[item["locus1_id"]]["latency_down"].insert(0, item["latency_median_1to2"])
                    temp[item["locus1_id"]]["latency_up"].insert(0, item["latency_median_2to1"])
        
        links = list()
        for index in temp:
            links.append(temp[index])

        return links

    def getWireless(self, server):
        macs = list(KPIWireless.objects.order_by().values("mac").distinct())

        wireless = list()
        for mac in macs:
            last_device_data = KPIWireless.objects.filter(Q(locus=server) & Q(mac=mac["mac"])).values().last()
            wireless.append(last_device_data)

        if wireless:
            response["wireless"] = wireless

    def orquestrate(self):
        raise NotImplementedError()