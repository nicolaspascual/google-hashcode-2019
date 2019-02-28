from src.photo import Photo

class FileLoader(object):
    def __init__(self, path):
        with open(path, 'r') as f:
            self.raw_statement = f.readlines()

    def parse(self):
        return self._parse()

    def _parse(self):
        res = []
        for photo_id, line in enumerate(self.raw_statement[1:]):
            type, _, *tags = line.strip().split(' ')
            res.append(Photo(photo_id, type, set(tags)))
        return res