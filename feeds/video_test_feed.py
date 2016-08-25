import gi
import os
import sys
import time
from .feed import Feed
gi.require_version('Gst', '1.0')
from gi.repository import Gst


class VideoTestFeed(Feed):
    def __init__(self, name, width, height, framerate):
        super().__init__(name)

        src = self.add_element('videotestsrc')
        convert = self.add_element('videoconvert')
        src.link(convert)

        self.add_video_shmsink(convert, width, height, framerate)


if __name__ == "__main__":
    os.environ["GST_DEBUG"] = '2'
    Gst.init(None)
    feed = VideoTestFeed('feed2', 1280, 720, '30/1')
    feed.play()

    while 1:
        time.sleep(2)
