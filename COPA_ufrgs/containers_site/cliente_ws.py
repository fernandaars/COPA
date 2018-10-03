import ssl
from threading import Thread

import websocket
from pylxd import *
from six.moves.urllib import parse

try:
    from ws4py.client import WebSocketBaseClient
    from ws4py.manager import WebSocketManager

    _ws4py_installed = True
except ImportError:  # pragma: no cover
    WebSocketBaseClient = object
    _ws4py_installed = False

from websocket import WebSocket


class MyWebSocket(WebSocket):
    def recv_frame(self):
        frame = super().recv_frame()
        print('yay! I got this frame: ', frame)
        return frame


def on_message(ws, message):
    print('>>>>>' + str(message))
    ws.send("ls -la")


def on_error(ws, error):
    print('>>>>>>>ERROR....' + str(error))


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("### opened ###")

    def run(*args):
        while True:
            dados = input()
            ws.send(dados)

    Thread(target=run).start()


if __name__ == "__main__":
    links_o = "ws://143.54.12.50:8010"
    ows = websocket.WebSocketApp(links_o,
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close)
    ows.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    o_wss = 'wss://143.54.12.164:8443'

    client = Client(endpoint='https://143.54.12.164:8443',
                    cert=('/home/ariel/containers_site/core/certfiles/lxd.crt',
                          '/home/ariel/containers_site/core/certfiles/lxd.key'),
                    verify=False)
    container = client.containers.get('testador')
    dados = {"command":            ["bash"],
             "environment":        {"HOME": "/root",
                                    "TERM": "xterm",
                                    "USER": "root"},
             "wait-for-websocket": True,
             "interactive":        True,
             "width":              20,
             "height":             20}  # Request Bash
    response = container.api['exec'].post(json=dados)  # manda request
    fds = response.json()['metadata']['metadata']['fds']

    operation_id = response.json()['operation'].split('/')[-1]
    parsed = parse.urlparse(
            client.api.operations[operation_id].websocket._api_endpoint)
    secret = '{}?secret={}'.format(parsed.path, fds['0'])

    print("secret", secret)

    o_link = o_wss + secret
    print("-----------------------------------------------------\n")
    print(o_link)
    print("\n-----------------------------------------------------\n")
