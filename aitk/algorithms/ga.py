# -*- coding: utf-8 -*-
# ****************************************************************
# aitk.algorithms: Algorithms for AI
#
# Copyright (c) 2021 AITK Developers
#
# https://github.com/ArtificialIntelligenceToolkit/aitk.algorithms
#
# ****************************************************************

import random
import math
from matplotlib import pyplot as plt

class GeneticAlgorithm(object):
    """
    A genetic algorithm is a model of biological evolution.  It
    maintains a population of chromosomes.  Each chromosome is
    represented as a list.  A fitness function must be
    defined to score each chromosome.  Initially, a random population
    is created. Then a series of generations are executed.  Each
    generation, parents are selected from the population based on
    their fitness.  More highly fit chromosomes are more likely to be
    selected to create children.  With some probability crossover will
    be done to model sexual reproduction.  With some very small
    probability mutations will occur.  A generation is complete once
    all of the original parents have been replaced by children.  This
    process continues until the maximum generation is reached or when
    the isDone method returns True.
    """

    def __init__(self, length, popSize, verbose=False):
        self.verbose = verbose      # Set to True to see more info displayed
        self.length = length        # Length of the chromosome
        self.popSize = popSize      # Size of the population
        self.maxGen = None          # Maximum generation
        self.pCrossover = None      # Probability of crossover
        self.pMutation = None       # Probability of mutation (per bit)
        self.pElite = None          # Percent elite
        self.generation = 0         # Current generation of evolution
        print("Genetic algorithm")
        print("  Chromosome length:", self.length)
        print("  Population size:", self.popSize)

    def initializePopulation(self):
        """
        Initialize each chromosome in the population with a random
        chromosome.

        Returns: None
        Result: Initializes self.population
        """
        self.bestEver = None        # Best member ever in this evolution
        self.bestEverScore = 0      # Fitness of best member ever
        self.population = None      # Population is a list of chromosomes
        self.scores = None          # Fitnesses of all members of population
        self.totalFitness = None    # Total fitness in entire population
        self.bestList = []          # Best fitness per generation
        self.avgList = []           # Avg fitness per generation
        self.population = []
        for i in range(self.popSize):
            chromosome = self.make_random_chromosome()
            self.population.append(chromosome)

    def reset(self):
        self.generation = 0

    def evaluatePopulation(self, **kwargs):
        """
        Computes the fitness of every chromosome in population.  Saves the
        fitness values to the list self.scores.  Checks whether the
        best fitness in the current population is better than
        self.bestEverScore. If so, updates this variable and saves the
        chromosome to self.bestEver.  Computes the total fitness of
        the population and saves it in self.totalFitness. Saves the
        current bestEverScore and the current average score to the
        lists self.bestList and self.avgList.

        Returns: None
        """
        self.scores = []
        for chromosome in self.population:
            self.scores.append(self.fitness(chromosome, **kwargs))
        bestScore = max(self.scores)
        best = self.population[self.scores.index(bestScore)]
        if bestScore > self.bestEverScore:
            self.bestEver = best[:]
            self.bestEverScore = bestScore
        self.report()
        self.totalFitness = sum(self.scores)
        self.bestList.append(self.bestEverScore)
        self.avgList.append(sum(self.scores)/float(self.popSize))

    def report(self):
        print("Generation %4d Best fitness %4.2f" % (self.generation,
                                                     self.bestEverScore))

    def selection(self):
        """
        Each chromosome's chance of being selected for reproduction is
        based on its fitness.  The higher the fitness the more likely
        it will be selected.  Uses the roulette wheel strategy.

        Returns: A COPY of the selected chromosome.
        """
        spin = random.random() * self.totalFitness
        partialSum = 0
        index = 0
        for i in range(self.popSize):
            partialSum += self.scores[i]
            if partialSum > spin:
                break
        return self.population[i][:]

    def crossover(self, parent1, parent2):
        """
        With probability self.pCrossover, recombine the genetic
        material of the given parents at a random location between
        1 and the length-1 of the chromosomes. If no crossover is
        performed, then return the original parents.

        Returns: Two children
        """
        if random.random() < self.pCrossover:
            crossPoint = random.randrange(1, self.length)
            if self.verbose:
                print("Crossing over at position", crossPoint)
            child1 = parent1[0:crossPoint] + parent2[crossPoint:]
            child2 = parent2[0:crossPoint] + parent1[crossPoint:]
            return child1, child2
        else:
            if self.verbose:
                print("No crossover performed")
            return parent1, parent2

    def mutation(self, chromosome):
        """
        With probability self.pMutation, mutate positions in the
        chromosome.

        Returns: None
        Result: Modifies the given chromosome
        """
        for i in range(self.length):
            if random.random() < self.pMutation:
                if self.verbose:
                    print("Mutating at position", i)
                gene = self.mutate_gene(chromosome[i])
                while chromosome[i] == gene:
                    gene = self.mutate_gene(chromosome[i])
                chromosome[i] = gene

    def oneGeneration(self):
        """
        Execute one generation of the evolution. Each generation,
        repeatedly select two parents, call crossover to generate
        two children.  Call mutate on each child.  Finally add both
        children to the new population.  Continue until the new
        population is full.

        Returns: None
        Result: Replaces self.pop with a new population.
        """
        # First, select the most elite to carry on unchanged:
        elite_size = math.floor(self.pElite * self.popSize)
        fittest = sorted(list(enumerate(self.scores)), key=lambda item: item[1],
                         reverse=True)
        newPop = []
        for i in range(elite_size):
            index, score = fittest[i]
            newPop.append(self.population[index])
        # Next, fill up rest of population:
        while len(newPop) < self.popSize:
            parent1 = self.selection()
            parent2 = self.selection()
            if self.verbose:
                print("Parents:")
                print(parent1)
                print(parent2)
            child1, child2 = self.crossover(parent1, parent2)
            self.mutation(child1)
            self.mutation(child2)
            if self.verbose:
                print("Children:")
                print(child1)
                print(child2)
            newPop.append(child1)
            newPop.append(child2)
        if len(newPop) > self.popSize:
            newPop.pop(random.randrange(len(newPop)))
        self.population = newPop
        self.generation += 1

    def evolve(self, maxGen, pCrossover=0.7, pMutation=0.001,
               pElite=0.0, **kwargs):
        """
        Run a series of generations until a maximum generation is
        reached or self.isDone() returns True.

        Returns the best chromosome ever found over the course of
        the evolution, which is stored in self.bestEver.
        """
        self.maxGen = maxGen
        self.pCrossover = pCrossover
        self.pMutation = pMutation
        self.pElite = pElite

        print("  Maximum number of generations:", self.maxGen)
        print("  Crossover rate:", self.pCrossover)
        print("  Mutation rate:", self.pMutation)
        print("  Elite percentage:", self.pElite)
        print("  Elite count:",
              math.floor(self.pElite * self.popSize))

        if self.generation == 0:
            self.initializePopulation()
            self.evaluatePopulation(**kwargs)

        while self.generation < self.maxGen and not self.isDone():
            self.oneGeneration()
            self.evaluatePopulation(**kwargs)
        if self.generation >= self.maxGen:
            print("Max generations reached")
        else:
            print("Solution found")
        return self.bestEver

    def plotStats(self, title=""):
        """
        Plots a summary of the GA's progress over the generations.
        """
        gens = range(len(self.bestList))
        plt.plot(gens, self.bestList, label="Best")
        plt.plot(gens, self.avgList, label="Average")
        plt.legend()
        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        if len(title) != 0:
            plt.title(title)
        plt.show()

    def make_random_chromosome(self):
        """
        Function to generate a new random chromosome.
        """
        return [self.make_random_gene() for i in range(self.length)]

    def mutate_gene(self, gene):
        """
        Function to mutate gene.
        """
        # Override this if needed
        return self.make_random_gene()

    def isDone(self):
        """
        If there is a stopping critera, it will be different for
        each problem. As a default, we do not stop until max
        epochs are reached.
        """
        # Override this if needed
        return False

    def fitness(self, chromosome, **kwargs):
        """
        The fitness function will change for each problem.  Therefore
        it is not defined here.  To use this class to solve a
        particular problem, inherit from this class and define this
        method.
        """
        # Override this
        pass

    def make_random_gene(self):
        """
        Function to generate a new random gene.
        """
        # Override this
        pass
