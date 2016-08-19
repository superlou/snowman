import gi
import os
import sys
import time
from feed import Feed
gi.require_version('Gst', '1.0')
from gi.repository import Gst


class ImageFeed(Feed):
    def __init__(self, name, image_path, width, height, framerate):
        super().__init__(name)

        src = self.add_element('filesrc')
        src.set_property('location', image_path)

        decode = self.add_element('pngdec')
        convert = self.add_element('videoconvert')
        scale = self.add_element('videoscale')
        freeze = self.add_element('imagefreeze')

        self.link_series(src, decode, convert, scale, freeze)
        self.add_video_shmsink(freeze, width, height, framerate)


if __name__ == "__main__":
    os.environ["GST_DEBUG"] = '2'
    Gst.init(None)
    feed = ImageFeed('feed3', '../media/lower_third2.png', 1280, 720, '30/1')
    feed.play()

    while 1:
        time.sleep(2)
