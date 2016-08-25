from manager.manager import Manager
from gui import SnowmanApp
from feeds import V4L2Feed, VideoTestFeed

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


if __name__ == "__main__":
    Gst.init(None)
    V4L2Feed('feed1', '/dev/video0', 1280, 720, '30/1').play()
    VideoTestFeed('feed2', 1280, 720, '30/1').play()
    manager = Manager('localhost', 9999)
    SnowmanApp(manager).run()
