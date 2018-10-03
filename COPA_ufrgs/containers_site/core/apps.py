import urllib3
from django.apps import AppConfig
from containers_site.COPA_general import *

urllib3.disable_warnings()


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        try:
            from .models import Pool, Container, Image

            Pool.objects.all().delete()
            Container.objects.all().delete()
            Image.objects.all().delete()

            server_list = get_server_list_by_file()
            print(server_list)
            containers = dict()
            for server in server_list:
                server = Pool(name=server,
                              local_ip=get_ip_by_name_by_file(server).split(":")[0])
                server.save()
                client = create_client(server.local_ip+":8443")

                containers[server] = client.containers.all()
            images = get_images_list()
            for image in images:
                Image(alias=image, fingerprint=images[image]).save()
                # TODO: ADD IMAGE LIST
        except Exception as e:
            print(str(e))

