#!/usr/bin/python3
from manager.manager import Manager
from feeds import V4L2Feed, VideoTestFeed, SvgFeed, ImageFeed, DskFeed
import multiprocessing

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


def create_manager():
    manager = Manager(('localhost', 9999))
    manager.start()

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

    f5 = DskFeed('feed5', 1280, 720, '30/1')
    f5.create_slide('media/lower_third.svg', {'line1': 'New Headline'})
    f5.select_slide(0)

    f5 = DskFeed('feed6', 1280, 720, '30/1')
    f5.create_slide('media/live.svg')
    f5.select_slide(0)

    multiprocessing.Process(target=create_manager).start()
