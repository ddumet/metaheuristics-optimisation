import numpy as np


from ga_operators import Selection_Tournament
from ga_operators import Crossover_Ordered
from ga_operators import Mutation_Swap, Mutation_Inversion
from ga_operators import Mutation_Scramble


class GA:
    '''
    The Genetic Algorithm.
    '''
    def __init__(self,
                 population=None,
                 nb_generation=100,
                 elite_ratio=0,
                 selection_op="tournament",
                 selection_params={
                     "K": 2
                     },
                 crossover_op="ordered",
                 crossover_params={"crossover_proba": 0.9,
                                   "sequence_max_width": 15},
                 mutation_op="scramble",
                 mutation_params={"mutation_proba": 0.1,
                                  "sequence_max_width": 5}):
        '''
        Parameters
        ----------
        - an already initialise population
        - the number of generation to produce
        - the ratio for elite individuals to keep to next generation
        - the selection operator for parents selection. One of:
            ("tournament")
        - selection_params: a dictionary of parameters for the selected
            selection operator
        - the crossover operator for generating offsprings. One of:
            ("ordered")
        - crossover_params: a dictionary of parameters for the selected
            crossover operator
        - the mutation operator for mutating offspring. One of:
            ("swap", "inversion", "scramble")
        - mutation_params: a dictionary of parameters for the selected
            mutation operator
        '''

        # NO VALIDATION on parameters for now ...

        # population
        self.population = population

        # Number of generation (default to 100)
        self.nb_generation = nb_generation

        # Number of Elites -> Parents to keep to
        # the next generation
        self.nb_elites = round(self.population.size * elite_ratio)

        # Number of offsprings to create (crossover)
        # at each generation -> population size - Elites
        self.nb_offsprings = self.population.size - self.nb_elites

        # Selection operators
        if selection_op == "tournament":
            self.selection_op = Selection_Tournament(selection_params)
        else:
            raise NotImplementedError

        # Crossover operators
        if crossover_op == "ordered":
            self.crossover_op = Crossover_Ordered(crossover_params)
        else:
            raise NotImplementedError

        # Mutation operators
        if mutation_op == "swap":
            self.mutation_op = Mutation_Swap(mutation_params)
        elif mutation_op == "inversion":
            self.mutation_op = Mutation_Inversion(mutation_params)
        elif mutation_op == "scramble":
            self.mutation_op = Mutation_Scramble(mutation_params)
        else:
            raise NotImplementedError

    def run(self):
        '''
        Do the thing !
        '''
        # get fitness of initial population
        self.population.get_fitness(self.population.individuals)

        # loop for all generation
        for _ in range(self.nb_generation):
            # Select parents according to the chosen selection operator
            # Same population size is generated (i.e. there could/ there
            # will be duplicated parents)
            parents = self.selection_op.select(self.population)

            # Generate offsprings through crossover
            # using the chosen crossover operator
            # The number of offsprings to generate depends on
            # the number of elites to keep for the next generation
            offsprings = self.crossover_op.crossover(parents,
                                                     self.nb_offsprings)

            # mutate offsprings using the chosen
            # mutation operator
            offsprings = self.mutation_op.mutate(offsprings)

            # Create Elites if we need to
            # Elites are the best individuals of the current
            # generation, i.e. the ones with the best fitness
            if self.nb_elites > 0:
                elites_idxs = \
                    np.argsort(self.population.fitness)[:self.nb_elites]
                elites = np.copy(self.population.individuals[elites_idxs])

                # Concatenate offsprings and elites to finally get a
                # full population matrix (population_size, dimension)
                offsprings = np.concatenate((elites, offsprings), axis=0)

            # update the population (solutions) and
            # fitness values
            self.population.get_fitness(offsprings)
