from src.slide import compare
from random import shuffle
from src.slide import Slide


class Slideshow(object):

    def __init__(self, slides):
        self._score = None
        self.slides = slides

    @property
    def score(self):
        if self._score is not None: return self._score
        self._score = 0
        for index in range(len(self.slides) - 1):
            self._score += compare(
                self.slides[index],
                self.slides[index + 1]
            )
        return self._score

    def __repr__(self):
        return ', '.join([repr(s) for s in self.slides])

    @staticmethod
    def random(photos):
        sequence = [Slide('H', p) for p in photos if p.type == 'H']

        vertical_shuffled = [p for p in photos if p.type == 'V']
        shuffle(vertical_shuffled)
        for i in range(0, len(vertical_shuffled) - 1, 2):
            sequence.append(
                Slide('V', vertical_shuffled[i], vertical_shuffled[i+1])
            )

        shuffle(sequence)
        return Slideshow(sequence)
