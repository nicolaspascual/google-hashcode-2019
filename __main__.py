from src.file_loader import FileLoader
from src.slide import Slide
from src.algorithms import SlidesGeneticAlgorithm
from src.slide import compare

photos = FileLoader('./resources/c_memorable_moments.txt').parse()

slideshow = SlidesGeneticAlgorithm(
    population_size=100,
    mutation_rate=.1,
    max_epochs=10000
).call(photos)

print(
    slideshow, slideshow.score
)
