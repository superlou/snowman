import gi
from gi.repository import GObject
import os
import sys
gi.require_version('Gst', '1.0')
from gi.repository import Gst


class Feed(object):
    def __init__(self, name):
        self.control_pipe_name = "/tmp/{0}-control-pipe".format(name)
        self.pipeline = Gst.Pipeline()

    def play(self):
        if os.path.exists(self.control_pipe_name):
            os.remove(self.control_pipe_name)

        self.pipeline.set_state(Gst.State.PLAYING)

    def add_element(self, element_name):
        element = Gst.ElementFactory.make(element_name, None)
        self.pipeline.add(element)
        return element

    def link_series(self, *elements):
        for i, element in enumerate(elements):
            if i == len(elements) - 1:
                break

            element.link(elements[i+1])

    def add_video_shmsink(self, last_element, width, height, framerate):
        shm_size = width * height * 4 * 22
        mixer_format = 'video/x-raw, format=BGRA, pixel-aspect-ratio=1/1, interlace-mode=progressive'

        sink = self.add_element('shmsink')
        sink.set_property('socket-path', self.control_pipe_name)
        sink.set_property('shm-size', shm_size)
        sink.set_property('wait-for-connection', 0)
        sink.set_property('sync', True)

        caps_string = "{0},width={1}, height={2}, framerate={3}".format(
            mixer_format, width, height, framerate)
        caps = Gst.caps_from_string(caps_string)

        last_element.link_filtered(sink, caps)
