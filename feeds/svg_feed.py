import gi
import os
import sys
from .feed import Feed
gi.require_version('Gst', '1.0')
from gi.repository import Gst


class SvgFeed(Feed):
    def __init__(self, name, svg_path, width, height, framerate):
        super().__init__(name)

        src = self.add_element('filesrc')
        src.set_property('location', svg_path)

        decode = self.add_element('rsvgdec')
        freeze = self.add_element('imagefreeze')
        convert = self.add_element('videoconvert')
        scale = self.add_element('videoscale')

        self.link_series(src, decode, freeze, convert, scale)
        self.add_video_shmsink(scale, width, height, framerate)
