class Dsk(object):
    next_id = 0

    def __init__(self, feed_id):
        self.id = Dsk.next_id
        Dsk.next_id += 1
        self.feed_id = feed_id
        self.active = False
