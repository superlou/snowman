import zmq
import threading
import json


class ManagerConnection(object):
    def __init__(self, server_port, publisher_port, callback=None):
        context = zmq.Context()
        address = "tcp://localhost"

        self.client_socket = context.socket(zmq.REQ)
        self.client_socket.connect('{}:{}'.format(address, server_port))

        self.subscriber_socket = context.socket(zmq.SUB)
        self.subscriber_socket.connect('{}:{}'.format(address, publisher_port))
        self.subscriber_socket.setsockopt(zmq.SUBSCRIBE, b'main')
        SubscriptionThread(self.subscriber_socket, callback).start()

    def send(self, json):
        self.client_socket.send_json(json)
        return self.client_socket.recv_json()


class SubscriptionThread(threading.Thread):
    def __init__(self, socket, callback):
        threading.Thread.__init__(self)
        self.socket = socket
        self.callback = callback

    def subscribe_json(self):
        multipart = self.socket.recv_multipart()
        obj = json.loads(multipart[1].decode('utf-8'))
        return obj

    def run(self):
        print("in thread")
        keep_running = True
        while keep_running:
            message = self.subscribe_json()
            print('subscriber:', message)

            if 'action' in message:
                action = message['action']

                if action == 'quit':
                    keep_running = False

            if 'update' in message:
                self.callback(message['update'], message['value'])
