class Photo(object):
    def __init__(self, photo_id, type, tags):
        self.photo_id = photo_id
        self.type = type
        self.tags = tags

    def __repr__(self):
        return f'Photo< {self.photo_id} {self.type} {self.tags}>'
