from random import sample, randint, random, shuffle
import numpy as np
from src.algorithms.genetic import Slideshow


class SlidesIndividual(object):

    def __init__(self, path):
        self.path = path
        self.fitness = None
        self.score = None

    def __repr__(self):
        return f'<SlidesIndividual({self.fitness}, {self.score}) {self.path}>'


class ISlidesGeneticAlgorithm(object):

    def __init__(self, population_size=100, mutation_rate=.01,
                 max_epochs=10000):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_epochs = max_epochs

    def call(self, photos):
        population = self.do_initialize_population(photos)
        self.do_calculate_fitness(population)

        i = 0
        fitnesses = []
        while not self.termination(i, fitnesses):

            new_population = []
            for _ in range(self.population_size):
                parents = self.do_pick_parents(population)
                child = self.do_crossover(*parents)
                child = self.do_mutation(child)
                new_population.append(child)

            self.do_calculate_fitness(new_population)
            population = self.do_next_generation(population, new_population)

            fitnesses.append(
                np.average([i.fitness for i in population])
            )

            i = i+1

        return sorted(population, key=lambda ind: ind.score)[0]

    def termination(self, i, fitnesses):
        """
        Termination condition for the GA. It will stop whenever it gets to a 
        maximun epochs or the last fitnesses are equal.

        Inputs:
            - i: Current iteration of the algorithm.
            - fitnesses: fitness in all the iterations
        Output:
            True if the termination condition is accomplished, False
            otherwise.
        """
        if i > 0:
            print(i, fitnesses[-1])
        if i >= self.max_epochs:
            print(
                f"Terminated due to maximum number of epochs reached ={self.max_epochs}")
            return True
        elif i >= 15 and all(f == fitnesses[-1] for f in fitnesses[-15:]):
            print("Terminated due to apparent convergence.")
            print(
                "More than 15 epochs have passed with no chane in individual average fitness")
            return True
        return False

    def do_initialize_population(self, n_cities):
        raise NotImplementedError()

    def do_calculate_fitness(self, population):
        raise NotImplementedError()

    def do_pick_parents(self, population):
        raise NotImplementedError()

    def do_crossover(self, *parents):
        raise NotImplementedError()

    def do_mutation(self, individual):
        raise NotImplementedError()

    def do_next_generation(self, olders, newers):
        raise NotImplementedError()


class SlidesGeneticAlgorithm(ISlidesGeneticAlgorithm):

    def do_initialize_population(self, photos):
        return [
            Slideshow.random(photos)
            for _ in range(self.population_size)
        ]

    def do_calculate_fitness(self, population):
        self.normalize_fitness(population)

    def normalize_fitness(self, population):
        total_score = sum([ind.score for ind in population])
        for individual in population:
            individual.fitness = individual.score / (total_score / 100)

    def do_pick_parents(self, population):
        return [self.pick_parent(population), self.pick_parent(population)]

    def pick_parent(self, population):
        """Performs the selection over the population by choosing at random based
        on the fitness of the individuals. That is an individual with high fitness
        has more probabilities of being picked.

        Arguments:
            population {List of TSPIndividual} -- Population with fitness calculated

        Returns:
            TSPIndividual -- Selected
        """

        counter = randint(0, 100)
        for individual in population:
            counter -= individual.fitness
            if counter <= 0:
                return individual
        return individual

    def do_crossover(self, *parents):
        """Performs a crossover among two parents, the crossover is designed to 
        pick a random range from the first parent, use it as it is and fill the 
        the remaining space with the cities left in the order of the second path

        [4,2,3,1]
                (pick from 1 to 2)[1,2,3,4]
        [3,2,1,4]

        Returns:
            List of TSPIndividual -- Parents to crossover
        """

        slide_sequence_1 = parents[0].slides
        slide_sequence_2 = parents[1].slides

        rand1 = randint(0, len(slide_sequence_1))
        rand2 = randint(0, len(slide_sequence_1))

        ini = min(rand1, rand2)
        end = max(rand1, rand2)

        new_slide_sequence = [-1 for _ in range(len(slide_sequence_2))]
        new_slide_sequence[ini:end] = slide_sequence_1[ini:end]

        new_sequence_set = set(new_slide_sequence)
        slide_sequence_2_removed_1 = [
            slide for slide in slide_sequence_2 if slide not in new_sequence_set
        ]

        last_i = 0
        for slide in slide_sequence_2_removed_1:
            for i in range(last_i, len(new_slide_sequence)):
                if new_slide_sequence[i] == -1:
                    new_slide_sequence[i] = slide
                    last_i = i
                    break

        return Slideshow(new_slide_sequence)

    def do_mutation(self, individual):
        """Performs a swap mutation in the path at random

        [ 1, 2, 3] -> [1, 3, 2]

        Arguments:
            individual {TSPIndividual} -- Individual to mutate

        Returns:
            TSPIndividual -- Mutated Individual
        """

        mut = 0
        while mut < len(individual.slides) and random() <= self.mutation_rate:
            origin = randint(0, len(individual.slides)-1)
            end = randint(0, len(individual.slides)-1)
            individual.slides[origin], individual.slides[end] =\
                individual.slides[end], individual.slides[origin]
            mut += 1
        return individual

    def do_next_generation(self, olders, newers):
        """
        Performs the strategy to select the future generation.

        Inputs:
            - olders: old generation.
            - newers: new generation.
        Output:
            Final population of the current epoch.
        """
        newpop = sorted(
            [*olders, *newers], key=lambda x: x.fitness,
            reverse=True
        )
        return newpop[:self.population_size]
