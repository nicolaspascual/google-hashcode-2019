from src.file_loader import FileLoader
from src.file_writer.writer import FileWriter

from src.slide import Slide
from src.algorithms import SlidesGeneticAlgorithm
from src.slide import compare

filename = 'a_example.txt'


photos = FileLoader('./resources/' + filename).parse()

slideshow = SlidesGeneticAlgorithm(
    population_size=100,
    mutation_rate=.1,
    max_epochs=10000
).call(photos)

FileWriter().write('./out/' + filename, slideshow)
