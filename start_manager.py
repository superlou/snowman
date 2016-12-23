#!/usr/bin/python3
from manager.manager import Manager
from feeds import V4L2Feed, VideoTestFeed, SvgFeed, ImageFeed, DskFeed

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


if __name__ == "__main__":
    Gst.init(None)

    manager = Manager(('localhost', 9999))
    manager.register_feed_type(V4L2Feed, 'v4l2')
    manager.register_feed_type(VideoTestFeed, 'video_test')
    manager.register_feed_type(DskFeed, 'dsk', play_after_create=False)

    manager.create_feed(0, 'v4l2', '/dev/video0')
    manager.create_feed(1, 'video_test')
    manager.create_feed(2, 'video_test').set_pattern(1)
    manager.create_feed(3, 'video_test').set_pattern(18)

    dsk = manager.create_feed(8, 'dsk')
    dsk.create_slide('media/lower_third.svg', {'line1': 'New Headline'})
    dsk.select_slide(0)

    dsk = manager.create_feed(9, 'dsk')
    dsk.create_slide('media/live.svg')
    dsk.select_slide(0)

    manager.start()
