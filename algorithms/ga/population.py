import numpy as np


class Population:
    '''
    A Population is the set of solutions evolving according
    to the 'evolution' algorithm.
    '''
    def __init__(self, problem, population_size):
        self.dim = problem.dim
        self.lbound = problem.lbound
        self.ubound = problem.ubound
        self.size = population_size
        self.generation = 0
        self.best_fitness = np.inf
        self.best_individual = 0

        self.logs = []

        # if discrete problem, use discrete_population
        # to generate the initial population
        if problem.type == "DISCRETE":
            self.individuals = self.get_discrete_population()
        else:
            self.individuals = self.get_continuous_population()
        self.fitness = np.zeros(problem.dim)
        self.fitness_func = problem.fitness

    def get_discrete_population(self):
        '''
        Create an initial random population of "discrete"
        individuals (i.e. each individual's gene is an integer,
        with no repetition of gene) of size population_size
        with each individual being of dimension self.dim
        Parameters:
        -----------
        - population_size: The size of the population, i.e. the
            number of individuals within the population
        Return:
        -------
        - m: A np.ndarray of dimension (population_size, dim)
            within the bounds of the problem
        '''
        # self.ubound + 1 -> because np.arange -> [start, end[
        rng = np.random.default_rng()
        m = rng.choice(np.arange(self.lbound, self.ubound + 1),
                       size=self.dim, replace=False)
        for _ in range(self.size - 1):
            m = np.concatenate((m,
                                rng.choice(np.arange(self.lbound,
                                                     self.ubound + 1),
                                           size=self.dim,
                                           replace=False)), axis=0)
        m = m.reshape(-1, self.dim)
        return(m)

    def get_continuous_population(self):
        '''
        Create an initial random population of "continuous"
        individuals (i.e. each individual's gene is a real) of size
        population_size with each individual being of dimension
        self.dim
        Parameters:
        -----------
        - population_size: The size of the population, i.e. the
            number of individuals within the population
        Return:
        -------
        - m: A np.ndarray of dimension (population_size, dim)
            within the bounds of the problem
        '''
        m = np.random.uniform(self.lbound,
                              self.ubound,
                              size=(self.size, self.dim))
        return(m)

    def get_fitness(self, individuals):
        '''
        Get the fitness for the current population from Problem
        class and store the result as self.fitness
        Return:
        -------
        - self.fitness: A np.ndarray of dimension (dim,)
        '''
        self.individuals = individuals
        self.fitness = self.fitness_func(self.individuals)

        # store some logs
        best_individual_idx = np.argsort(self.fitness)[0]
        best_fitness = self.fitness[best_individual_idx]
        best_individual = self.individuals[best_individual_idx]
        fitness_mean = self.fitness.mean()

        self.logs.append([self.generation, best_fitness,
                          best_individual, fitness_mean])
        self.generation = self.generation + 1

        # Update all time best
        if best_fitness < self.best_fitness:
            self.best_fitness = best_fitness
            self.best_individual = best_individual

        return(self.fitness)
