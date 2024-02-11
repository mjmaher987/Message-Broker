import websocket
import argparse
import threading
import logging
import json
import requests


def parse_args():
    parser = argparse.ArgumentParser(description='Server connection arguments')
    parser.add_argument('--coordinator_ip', type=str, default='127.0.0.1', help='IP address of the Coordinator')
    parser.add_argument('--coordinator_port', type=str, default='7000', help='Port of the Coordinator')
    parser.add_argument('--coordinator_backup_ip', default=None, type=str, help='IP address of the backup Coordinator')
    parser.add_argument('--coordinator_backup_port', default=None, type=str, help='Port of the backup Coordinator')
    args = parser.parse_args()

    return args


class Node:
    def __init__(self, coordinator_ip, coordinator_port):
        self.coordinator_ip = coordinator_ip
        self.coordinator_port = coordinator_port
        self.base_url = f'http://{self.coordinator_ip}:{self.coordinator_port}'
        self.ws_url = f'ws://{self.coordinator_ip}:{self.coordinator_port}/ws'

        logging.basicConfig(filename='client.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(lineno)d %(name)s %(message)s')
        self.logger = logging.getLogger(__name__)

    def on_message(self, ws, message):
        if type(message) == bytes:
            return
        data = json.loads(message)
        if 'type' in data:
            if data['type'] == 'ping':
                ws.send(json.dumps({'type': 'pong'}))
                return
            else:
                self.logger.info('WS received:', data)
            # elif data['type'] == 'send_message':
            #     message = data['message']
            #     # m_type = message['type']

    def on_error(self, ws, error):
        self.logger.error(error)

    def on_close(self, ws):
        self.logger.info("WebSocket closed")

    def on_open(self, ws):
        self.logger.info("WebSocket opened")

    def connect(self):
        response = requests.post(self.base_url + '/connect/')
        if response.status_code == 200:
            self.id = json.loads(response.content)

            self.ws = websocket.WebSocketApp(f'{self.ws_url}/',
                                             cookie=f'id={self.id}',
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close,
                                             on_open=self.on_open)
            wst = threading.Thread(target=self.ws.run_forever)
            wst.daemon = True
            wst.start()
            while True:
                pass
        else:
            self.logger.error('Could not establish a connection')


if __name__ == '__main__':
    args = parse_args()

    node = Node(args.coordinator_ip, args.coordinator_port)
    node.connect()