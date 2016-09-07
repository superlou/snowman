import socket
import re
import time
import math
import zmq
import json
from .dsk import Dsk


class Manager(object):
    def __init__(self, snowmix_address):
        self.snowmix_address = snowmix_address
        self.snowmix = self.connect_to_snowmix(snowmix_address)

        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5555")
        self.server_socket = socket

        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:5556")
        self.publisher_socket = socket

        self.framerate = 30.
        self.preview = 1
        self.program = 2
        self.dsks = [Dsk(feed_id) for feed_id in [5, 6, 7, 8]]
        self.hide_all_dsks()
        self.update_main_bus()

    def start(self):
        keep_running = True

        while keep_running:
            message = self.server_socket.recv_json()
            print('message:', message)

            if 'action' in message:
                action = message['action']

                if action == 'transition':
                    self.transition()
                elif action == 'set_program':
                    self.set_program(message['feed'])
                elif action == 'set_preview':
                    self.set_preview(message['feed'])
                elif action == 'toggle_dsk':
                    self.toggle_dsk(message['dsk_id'])
                elif action == 'quit':
                    keep_running = False
                    self.publish_json({'action': 'quit'})

            self.server_socket.send_json({'response': 'ok'})

    def publish_json(self, obj):
        message = bytes(json.dumps(obj), 'utf-8')
        self.publisher_socket.send_multipart([b'main', message])

    def connect_to_snowmix(self, address):
        snowmix = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            snowmix.connect(address)
        except:
            print("Unable to connect to Snowmix at {0}:{1}".format(*address))

        snowmix.recv(4096)  # Clear out version string
        return snowmix

    def hide_all_dsks(self):
        for dsk_feed in self.dsks:
            self.send_command('vfeed alpha {} 0'.format(dsk_feed.feed_id))

        self.active_dsks = []

    def cut_in_dsk(self, dsk_id):
        self.send_command('vfeed alpha {} 1'.format(self.dsks[dsk_id].feed_id))
        self.dsks[dsk_id].active = True
        self.notify('active_dsks', self.get_active_dsk_ids())

    def cut_out_dsk(self, dsk_id):
        self.send_command('vfeed alpha {} 0'.format(self.dsks[dsk_id].feed_id))
        self.dsks[dsk_id].active = False
        self.notify('active_dsks', self.get_active_dsk_ids())

    def get_active_dsk_ids(self):
        return [feed.id for feed in self.dsks if feed.active]

    def build_dsk_feeds_list(self):
        return " ".join([str(feed.feed_id) for feed in self.dsks])

    def toggle_dsk(self, dsk_id):
        if self.dsks[dsk_id].active:
            self.cut_out_dsk(dsk_id)
        else:
            self.cut_in_dsk(dsk_id)

    def subscribe(self, callback):
        self.callback = callback

    def notify(self, target, value):
        self.publish_json({'update': target, 'value': value})

    def set_preview(self, feed):
        self.preview = feed
        self.update_main_bus()

    def set_program(self, feed=None):
        if feed:
            self.program = feed
        else:
            self.program, self.preview = self.preview, self.program

        self.update_main_bus()

    def update_main_bus(self):
        self.send_command('vfeed alpha {0} 0'.format(self.preview))
        self.send_command('vfeed alpha {0} 1'.format(self.program))
        self.send_command('tcl eval SetFeedToOverlay {0} {1} {2}'.format(
                          self.program,
                          self.preview,
                          self.build_dsk_feeds_list()
                          ))

        self.notify('preview', self.preview)
        self.notify('program', self.program)

    def transition(self, duration=0.25):
        frames = math.ceil(duration * self.framerate)
        delta = 1. / frames
        self.send_command('vfeed move alpha {0} {1} {2} {3}'.format(
                          self.preview,
                          delta,
                          frames,
                          self.build_dsk_feeds_list()
                          ))

        time.sleep(duration)
        self.set_program()

    def send_command(self, command, responds=False):
        self.snowmix.send(bytearray(command + '\n','utf-8'))

        if responds:
            return self.receive_all()
        else:
            return None

    def get_feed_ids(self):
        self.snowmix.send(b'feed list\n')
        response = self.receive_all()
        feed_pattern = re.compile(r"Feed ID ([\d]+)", re.MULTILINE)
        matches = feed_pattern.findall(response)
        return [int(string_id) for string_id in matches]

    def receive_all(self):
        result = ''

        while 1:
            data = self.snowmix.recv(4096)

            if len(data) == 0:
                break

            result += data.decode('utf-8')

            if result.endswith(('STAT: \n', 'MSG: \n')):
                break

        return result
