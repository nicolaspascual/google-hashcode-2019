from src.algorithms import Slideshow

class FileWriter(object):
    def write(self, filename, slideshow):
        return self._write(filename, slideshow)

    def _write(self, filename, slideshow):
        out = open(filename, 'w+')
        out.write(str(len(slideshow.slides)) + '\n')
        for slide in slideshow.slides:
            ids = ''
            for photo in slide.photos:
                ids += str(photo.photo_id) + ' '
            new_line = ids[:-1] + '\n'
            out.write(new_line)
        out.close()
