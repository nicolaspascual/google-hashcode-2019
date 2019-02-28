from src.file_loader import FileLoader
from src.slide import Slide
from src.algorithms import SlidesGeneticAlgorithm

photos = FileLoader('./resources/b_lovely_landscapes.txt').parse()

slideshow = SlidesGeneticAlgorithm(
    population_size=10,
    mutation_rate=.01,
    max_epochs=10000
).call(photos)

print(
    slideshow, slideshow.score
)
