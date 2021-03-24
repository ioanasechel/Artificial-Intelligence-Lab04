import random


class Chromosome:
    def __init__(self, params=None):
        self.__params = params
        self.__route = random.sample(self.__params['vertices'], self.__params['noV'])
        self.__fitness = self.__params['fitness'](self.__route)

    @property
    def repres(self):
        return self.__route

    @property
    def fitness(self):
        return self.__fitness.get_fitness()

    @repres.setter
    def repres(self, l=[]):
        self.__route = l

    @fitness.setter
    def fitness(self, fit=0.0):
        # self.__fitness.set_fitness(fit)
        self.__fitness = fit

    def crossover(self, c):
        # ordered crossover
        child = []
        childP1 = []
        childP2 = []

        geneA = int(random.random() * len(self.__route))
        geneB = int(random.random() * len(c.repres))

        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        # randomly select a subset of the first parent string
        for i in range(startGene, endGene):
            childP1.append(self.__route[i])

        # fill the remainder of the route with the genes from the second parent in the order in which they appear,
        # without duplicating any genes in the selected subset from the first parent
        childP2 = [item for item in c.repres if item not in childP1]

        child = childP1 + childP2

        self.__route = child
        return self

    def mutation(self):
        # swap mutation -> with specified low probability, two cities will swap places in our route
        for swapped in range(len(self.__route)):
            x = random.random()
            if x < self.__params['mutationRate']:
                swapWith = int(random.random() * len(self.__route))

                node1 = self.__route[swapped]
                node2 = self.__route[swapWith]

                self.__route[swapped] = node2
                self.__route[swapWith] = node1

    def __str__(self):
        return '\n Chromo: ' + str(self.__route) + ' has fit: ' + str(self.__fitness)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, c):
        return self.__route == c.__repres and self.__fitness == c.__fitness
