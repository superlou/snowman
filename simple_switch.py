#!/usr/bin/python3
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

    f3 = VideoTestFeed('feed3', 1280, 720, '30/1')
    f3.play()
    f3.set_pattern(1)

    f4 = VideoTestFeed('feed4', 1280, 720, '30/1')
    f4.play()
    f4.set_pattern(18)

    manager = Manager('localhost', 9999)
    SnowmanApp(manager).run()
