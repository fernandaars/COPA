from pylxd import Client
from django.apps import AppConfig


COPA_HOME = "/copa/COPA/"
SERVS_HOME = COPA_HOME + ""  # Location of the `servers.txt` file.
CERT_HOME = COPA_HOME + "certs/"  # Location of the lxd certificates and keys.
COPA_HOST = "127.0.0.1"  # COPA's host IP address.
IMAGE_HOST = "127.0.0.1"  # Image pool.


def get_server_list_by_file():  # just used in first COPA execution
    fx = open(SERVS_HOME + "servers.txt")
    reader = fx.read()
    lines = reader.split("\n")
    servers = []
    for item in lines:
        it = item.split(";")
        if it[0] != "":
            servers.append(it[0])
    return servers


def get_ip_by_name_by_file(name):  # just used in first COPA execution
    names = {}
    fx = open(SERVS_HOME + "servers.txt")
    reader = fx.read()
    lines = reader.split("\n")
    for item in lines:
        it = item.split(";")
        if it[0] != "":
            names[it[0]] = it[1]
    return names[name]


def get_server_list():
    from core.models import Pool
    servers = []
    obj = Pool.objects.all()
    for o in obj:
        servers.append(o.name)
    return servers


def get_images_list():
    images = {}
    aliases = []
    cp_c = 0
    client = create_client(IMAGE_HOST + ":8443")
    all_images = client.images.all()
    for i in all_images:
        for item in i.aliases:
            aliases.append(item["name"])
    for i in all_images:
        if len(i.aliases) > 0 and i.fingerprint is not None:
            images[aliases[cp_c]] = i.fingerprint
            cp_c = cp_c + 1
    return images


def get_ip_by_name(param_name):
    from core.models import Pool
    names = {}
    obj = Pool.objects.get(name=param_name)
    if obj.local_ip.find(':') >= 0:
        return obj.local_ip
    else:
        return obj.local_ip + ':8443'


def create_client(server_addr):
    client = Client(endpoint="https://" + server_addr,
                    cert=(CERT_HOME + "lxd.crt", CERT_HOME + "lxd.key"),
                    verify=False)
    return client
