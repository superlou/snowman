import socket
import re


class Manager(object):
    def __init__(self, host='localhost', port=9999):
        snowmix = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.snowmix = snowmix

        try:
            snowmix.connect((host, port))
        except:
            print("Unable to connect to Snowmix at {0}:{1}".format(host, port))

        self.snowmix.recv(4096)  # Clear out version string

        self.preview = 1
        self.program = 2
        self.update_main_bus()

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
        self.send_command('tcl eval SetFeedToOverlay {0} {1}'.format(self.program, self.preview))

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
