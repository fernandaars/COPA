from containers_site.COPA_general import *
from django.core import *
from django.db import models
from django.conf import settings
from core.models import Container, Pool
import datetime
import time
import json

if __name__ == "django.core.management.commands.shell":
    # refresh container status
    while True:
        servers = get_server_list()
        Container.objects.all().delete()
        for i in servers:
            ip = get_ip_by_name(i)
            cl = create_client(ip)
            c_all = cl.containers.all()
            opool = Pool(name=i)
            for c in c_all:
                obj = Container(name=c.name, pool=opool)
                obj.pool = opool
                obj.name = c.name
                obj.status = c.status
                # 2017-08-17T18:37:09Z
                obj.created = datetime.datetime.strptime(c.created_at,
                                                         '%Y-%m-%dT%H:%M:%SZ')
                obj.description = c.description
                info = c.state()
                obj.pid = info.pid
                obj.usage_memory = info.memory["usage"]
                obj.usage_memory_peak = info.memory["usage_peak"]
                obj.usage_swap = int(info.memory["swap_usage"])
                obj.usage_swap_peak = info.memory["swap_usage_peak"]
                obj.cpu_usage = 0
                obj.processes = info.processes
                obj.last_update = datetime.datetime.now()
                obj.full_network_info = json.dumps(info.network)
                obj.save()
        time.sleep(45)
