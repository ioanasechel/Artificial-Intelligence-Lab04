import operator
import copy
import pandas as pd
import random
from Chromosome import Chromosome
import matplotlib.pyplot as plt
import numpy as np


class GA:
    def __init__(self, problParam=None):
        self.__params = problParam
        self.__population = []
        self.initialisation()

    # To simulate our “survival of the fittest”, we can make use of Fitness to rank each individual in the population.
    # Our output will be an ordered list with the route IDs and each associated fitness score.
    def ordered_population_ranks(self):
        fitness_results = {}
        for i in range(0, len(self.__population)):
            fitness_results[i] = self.__population[i].fitness
        return sorted(fitness_results.items(), key=operator.itemgetter(1), reverse=True)

    @property
    def population(self):
        return self.__population

    # make our initial population
    def initialisation(self):
        for _ in range(0, self.__params['popSize']):
            c = Chromosome(self.__params)
            self.__population.append(c)

    def evaluation(self):
        for c in self.__population:
            c.fitness = self.__params['fitness'](c.repres)

    def best_chromosome(self):
        best = self.__population[0]
        for c in self.__population:
            if c.fitness > best.fitness:
                best = c
        return best

    def worst_chromosome(self):
        worst = self.__population[0]
        for c in self.__population:
            if c.fitness < worst.fitness:
                worst = c
        return worst

    def selection(self):
        # fitness proportionate selection (aka “roulette wheel selection”)
        selection = []
        selection_results = []
        pop_ranked = self.ordered_population_ranks()

        # set up the roulette wheel by calculating a relative fitness weight for each individual
        df = pd.DataFrame(np.array(pop_ranked), columns=["Index", "Fitness"])
        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

        # we want to hold on to our best routes so we use elitism
        for i in range(0, self.__params['eliteSize']):
            selection_results.append(pop_ranked[i][0])

        # compare a randomly drawn number to these weights to select our mating pool
        # returns a list of route IDs, which we can use to create the mating pool
        for _ in range(0, len(pop_ranked) - self.__params['eliteSize']):
            pick = 100 * random.random()
            for i in range(0, len(pop_ranked)):
                if pick <= df.iat[i, 3]:
                    selection_results.append(pop_ranked[i][0])
                    break

        # extracting the selected individuals from our population
        for i in range(0, len(selection_results)):
            index = selection_results[i]
            selection.append(self.__population[index])
        return selection

    def nextGeneration(self):
        selection = self.selection()
        new_population = []
        pool = random.sample(selection, len(selection))

        # use elitism to retain the best routes from the current population
        for i in range(0, self.__params['eliteSize']):
            new_population.append(copy.copy(selection[i]))

        # we use the crossover function to fill out the rest of the next generation
        for i in range(0, len(selection) - self.__params['eliteSize']):
            child = pool[i].crossover(pool[len(selection) - i - 1])
            child.mutation()
            # child.mutation()
            new_population.append(child)

        self.__population = new_population
        self.evaluation()

    def oneGeneration(self):
        newPop = []
        for _ in range(self.__params['numberOfChromosomes']):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            newPop.append(off)
        self.__population = newPop
        self.evaluation()

    def oneGenerationElitism(self):
        newPop = [self.bestChromosome()]
        for _ in range(self.__params['numberOfChromosomes'] - 1):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            newPop.append(off)
        self.__population = newPop
        self.evaluation()

    def oneGenerationSteadyState(self):
        for _ in range(self.__params['numberOfChromosomes']):
            p1 = self.__population[self.selection()]
            p2 = self.__population[self.selection()]
            off = p1.crossover(p2)
            off.mutation()
            off.fitness = self.__params['function'](off.repres, self.__params)
            worst = self.worstChromosome()
            if off.fitness < worst.fitness:
                worst = off
