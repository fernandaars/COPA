import sys
from urllib.parse import urlparse

from websocket import WebSocket
from containers_site.COPA_general import *

try:
    from ws4py.client import WebSocketBaseClient
    from ws4py.manager import WebSocketManager

    _ws4py_installed = True
except ImportError:
    WebSocketBaseClient = object
    _ws4py_installed = False


# DEFAULTS


class MyWebSocket(WebSocket):
    def recv_frame(self):
        frame = super(MyWebSocket, self).recv_frame()
        print('I got this frame: ', frame)
        return frame


if __name__ == "__main__":
    print(sys.argv)
    o_wss = 'wss://' + sys.argv[1]

    client = Client(endpoint=sys.argv[2],
                    cert=(CERT_HOME + 'lxd.crt', CERT_HOME + 'lxd.key'),
                    verify=False)
    container = client.containers.get(sys.argv[3])
    dados = {"command":            ["bash"],
             "environment":        {"HOME": "/root",
                                    "TERM": "xterm",
                                    "USER": "root"},
             "wait-for-websocket": True,
             "interactive":        True,
             "width":              120, "height": 25}
    response = container.api['exec'].post(json=dados)
    fds = response.json()['metadata']['metadata']['fds']

    operation_id = response.json()['operation'].split('/')[-1]
    prsd = urlparse(client.api.operations[operation_id].websocket._api_endpoint)
    secret = '{}?secret={}'.format(prsd.path, fds['0'])

    o_link = o_wss + secret
    print("keys=" + o_link)
