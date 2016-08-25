import gi
import os
import sys
import time
from .feed import Feed
gi.require_version('Gst', '1.0')
from gi.repository import Gst


class V4L2Feed(Feed):
    def __init__(self, name, device, width, height, framerate):
        super().__init__(name)

        src = self.add_element('v4l2src')
        src.set_property('device', device)

        convert1 = self.add_element('videoconvert')
        scale = self.add_element('videoscale')
        convert2 = self.add_element('videoconvert')

        self.link_series(src, convert1, scale, convert2)
        self.add_video_shmsink(convert2, width, height, framerate)


if __name__ == "__main__":
    os.environ["GST_DEBUG"] = '2'
    Gst.init(None)
    feed = V4L2Feed('feed1', '/dev/video0', 1280, 720, '30/1')
    feed.play()

    while 1:
        time.sleep(2)
