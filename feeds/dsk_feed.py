# Requires Inkscape
import gi
import os
import sys
from .feed import Feed
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from subprocess import call
import uuid
from lxml import etree


class DskFeed(Feed):
    SLIDE_BASE_PATH = '/tmp/slides'
    DEFAULT_SLIDE_PATH = 'frames/empty-1280x720.png'

    def __init__(self, name, width, height, framerate):
        super().__init__(name)
        self.width = width
        self.height = height
        self.slides = []

        if not os.path.exists(DskFeed.SLIDE_BASE_PATH):
            os.makedirs(DskFeed.SLIDE_BASE_PATH)

        src = self.add_element('filesrc')
        self.src = src
        # src.set_property('location', image_path)

        decode = self.add_element('pngdec')
        convert = self.add_element('videoconvert')
        scale = self.add_element('videoscale')
        freeze = self.add_element('imagefreeze')

        self.link_series(src, decode, convert, scale, freeze)
        self.add_video_shmsink(freeze, width, height, framerate)

    def create_slide(self, svg_path, substitutions={}):
        slide = DskSlide(svg_path, self.width, self.height, substitutions)
        self.slides.append(slide)

    def select_slide(self, slide_id):
        self.stop()
        self.src.set_property('location', self.slides[slide_id].slide_file)
        self.play()

class DskSlide(object):
    def __init__(self, base_svg_path, width, height, substitutions):
        self.base_svg_path = base_svg_path
        self.substitutions = substitutions

        name = str(uuid.uuid1())

        if substitutions:
            tree = etree.parse(self.base_svg_path)
            tree = self.alter_svg(tree, substitutions)
            tree_xml = etree.tostring(tree, encoding='unicode')
            temp_svg = open('/tmp/temp.svg', 'w')
            temp_svg.write(tree_xml)
            temp_svg.close()

            svg_path = '/tmp/temp.svg'
        else:
            svg_path = self.base_svg_path

        slide_file = os.path.join(DskFeed.SLIDE_BASE_PATH, name + '.png')
        self.slide_file = slide_file
        call(['inkscape', svg_path,
              '--export-png', slide_file,
              '--export-width', str(width),
              '--export-height', str(height)])

    def alter_svg(self, tree, substitutions):
        nsmap = {
            'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
            'cc': 'http://web.resource.org/cc/',
            'svg': 'http://www.w3.org/2000/svg',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'xlink': 'http://www.w3.org/1999/xlink',
            'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'inkscape': 'http://www.inkscape.org/namespaces/inkscape'
            }

        for text_id, new_value in substitutions.items():
            selector = "//svg:text[@id='{}']/svg:tspan".format(text_id)
            result = tree.xpath(selector, namespaces=nsmap)

            if len(result) == 1:
                tspan = result[0]
                tspan.text = new_value

        return tree
