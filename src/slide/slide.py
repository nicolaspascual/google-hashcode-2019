

class Slide(object):

    def __init__(self, type, *photos):
        self.type = type
        self.photos = photos

        if len(photos) == 0 or (type == 'V' and len(photos) != 2) or (type == 'H' and len(photos) != 1):
            raise ValueError('Not right number of photos')

    @property
    def tags(self):
        tags = [p.tags for p in self.photos]
        return set([item for sublist in tags for item in sublist])

    def __repr__(self):
        return f'<Slide {self.photos}>'
