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

            if result.endswith('STAT: \n'):
                break

        return result
