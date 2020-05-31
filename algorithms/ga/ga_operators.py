import numpy as np


# -------------------
# SELECTION OPERATORS
# -------------------
class Selection_Proportionate:
    '''
    Proportionate selection operator
    ***WARNING***: This operator will NOT give the expected
    results cases where fitness values can be negative.
    Another operator must be used in this case.

    Possible implementation TRICK:
    When you have negative values, you could try to find the smallest
    fitness value in your population and add its opposite to every
    value. This way you will no longer have negative values, while
    the differences between fitness values will remain the same.
    '''
    pass


class Selection_Stochastic_Universal_Sampling:
    pass


class Selection_Ranking:
    '''
    Ranking selection operator
    '''
    pass


class Selection_Fitness_Scaling:
    pass


class Selection_Tournament:
    '''
    Tournament selection operator:
    1. Random uniform select of K individuals
    2. Select the fittest of these K individuals
    3. Repeat 1., 2. until the reach the desired number of individuals
    '''
    def __init__(self, selection_params):
        '''
        Parameters
        ----------
        selection_parameters includes:
        - selective pressure K, used to select number of individual
            per tournament. The higher K, the more probability the best
            individuals will be selected (-> loss of diversity).
            A recommended value is 2.
        '''
        self.K = selection_params["K"]

    def select(self, population):
        '''
        Parameters
        ----------
        - The current population instance
        Return
        ------
        - a numpy array, selection of individuals to serve for reproduction
            (crossover)
        '''
        selection_idxs = []
        for _ in range(population.size):
            # Select K individuals by index
            idxs = np.random.choice(range(population.size),
                                    size=self.K,
                                    replace=False)

            # Get the best individual (best fitness) by argsort-ing the
            # fitness vector (population.fitness)
            # we are expecting minimisation problem, best fitness is index 0
            best_idx = idxs[np.argsort(population.fitness[idxs])[0]]
            selection_idxs.append(best_idx)

        # Return the selected individuals
        return(population.individuals[np.array(selection_idxs)])


# -------------------
# CROSSOVER OPERATORS
# -------------------
class Crossover_Ordered:
    '''
    Ordered crossover operator:
    Loop for nb_offsprings to be generated
    1. Select (uniform random) two parents from the entire population
    2. Roll a (uniform!) dice ! If probability is < than
        crossover_proba then perform crossover.
        Else the two parents are kept as if for the next generation.
    3. Select (uniform random) two crossover points that defines a
        sequence of genes to crossover
    4. Copy sequence from parent1 to child2 and parent2 to child1
    5. Complete child1 sequence with parent1, child2 with parent2
    '''
    def __init__(self, crossover_params):
        '''
        - the crossover probability
        - the width of the sequence of genes to crossover
        '''
        self.crossover_proba = crossover_params["crossover_proba"]
        self.max_width = crossover_params["sequence_max_width"]

    def crossover(self, parents, nb_offsprings):
        '''
        Perform the crossover
        Parameters
        ----------
        - all parents that have been selected for crossover
            as numpy ndarray
        - the number of offsprings to generate. That depends on the
            ratio of elite individuals that will be kept for next
            generation.
        Return
        ------
        - the offsprings as a numpy ndarray
        '''
        rng = np.random.default_rng()
        parents_size = parents.shape[0]
        dim = parents.shape[1]
        current_nb_offsprings = 0
        while current_nb_offsprings < nb_offsprings:
            # randomly (uniform) select two parents
            # by selecting two indexes from the
            # parents array (with no repetition)
            parents_idx = rng.choice(parents_size, size=2, replace=False)
            parent1 = parents[parents_idx][0]
            parent2 = parents[parents_idx][1]

            # Probability of performing crossover
            # if < self.crossover_proba perform cross over
            # for these 2 parents
            if rng.uniform() < self.crossover_proba:

                # randomly (uniform) select two crossover points
                # distant within [2, self.max_witdh]
                invalid_sequence = True
                while invalid_sequence:
                    seq = np.sort(rng.choice(dim, size=2, replace=False))
                    if ((seq[1] - seq[0]) <= self.max_width) and\
                       ((seq[1] - seq[0]) > 1):
                        invalid_sequence = False

                # initialise a child1, child2 array
                child1 = -1*np.ones(dim, dtype=np.int32)
                child2 = -1*np.ones(dim, dtype=np.int32)

                # copy the genes between crossover points
                # from parents1 to child2 and parents2 to child1
                child1[seq[0]:seq[1]] = parent2[seq[0]:seq[1]]
                child2[seq[0]:seq[1]] = parent1[seq[0]:seq[1]]

                # complete the child1 with parent1 and child2 with
                # parent2
                child1 = self.complete_sequence(child1, parent1, seq, dim)
                child2 = self.complete_sequence(child2, parent2, seq, dim)
            # else, we keep parents as-is for next generation
            else:
                child1 = np.copy(parent1)
                child2 = np.copy(parent2)

            # adding children to the array of offsprings
            if current_nb_offsprings == 0:
                offsprings = child1
                offsprings = np.concatenate((offsprings, child2), axis=0)
                current_nb_offsprings = current_nb_offsprings + 2
            elif current_nb_offsprings <= (nb_offsprings - 2):
                offsprings = np.concatenate((offsprings, child1), axis=0)
                offsprings = np.concatenate((offsprings, child2), axis=0)
                current_nb_offsprings = current_nb_offsprings + 2
            else:
                offsprings = np.concatenate((offsprings, child1), axis=0)
                current_nb_offsprings = current_nb_offsprings + 1

        # reshape offsprings to a (self.nb_offsprings, dimension)
        # array
        offsprings = offsprings.reshape(-1, dim)

        return(offsprings)

    def complete_sequence(self, child, parent, cx_point, d):
        idx_child = idx_parent = cx_point[1]
        not_complete = True
        # complete upper range of the sequence first
        while not_complete:
            # for idx in range(cx_point[1], dim):
            if parent[idx_parent] not in child:
                child[idx_child] = parent[idx_parent]
                if idx_child == (d-1):
                    idx_child = 0
                else:
                    idx_child = idx_child + 1
            if idx_parent == (d-1):
                idx_parent = 0
            else:
                idx_parent = idx_parent + 1
            # testing if sequence is complete
            # i.e. idx_child = cx_point[0]
            if idx_child == cx_point[0]:
                not_complete = False
        return(child)


# ------------------
# MUTATION OPERATORS
# ------------------
class Mutation_Swap:
    '''
    The Swap Mutation operator: Two genes are randomly selected
    and swapped together.
    '''
    def __init__(self, mutation_params):
        '''
        Parameters:
        -----------
        - the mutation probability
        '''
        self.mutation_proba = mutation_params["mutation_proba"]

    def mutate(self, offsprings):
        '''
        Perform the swap mutation for all offsprings
        1. roll a (uniform!) dice ! If probability is < than
            mutation_proba then perform mutation.
        2. select (random uniform) two genes (indices)
        3. swap them
        Parameters
        ----------
        - the offsprings (as a numpy array) on which to apply
            the mutation
        Return
        ------
        - the modified offsprings (althought not necessary as mutation
            is done inplace)
        '''
        rng = np.random.default_rng()
        nb_offsprings = offsprings.shape[0]
        dim = offsprings.shape[1]

        for i in range(nb_offsprings):
            # Probability of performing mutation
            # if < self.mutation_proba perform mutation
            # else NO mutation for this offspring
            if rng.uniform() < self.mutation_proba:
                idxs = rng.choice(dim, size=2, replace=False)
                temp = offsprings[i][idxs[0]]
                offsprings[i][idxs[0]] = offsprings[i][idxs[1]]
                offsprings[i][idxs[1]] = temp

        return(offsprings)


class Mutation_Inversion:
    '''
    The Inversion Mutation operator: A sequence of genes is
    randomly selected and inversed
    '''
    def __init__(self, mutation_params):
        '''
        Parameters:
        -----------
        - the mutation probability
        - the width of the sequence of genes on which to apply
        inversion
        '''
        self.mutation_proba = mutation_params["mutation_proba"]
        self.max_width = mutation_params["sequence_max_width"]

    def mutate(self, offsprings):
        '''
        Perform the inversion mutation for all offsprings
        1. roll a (uniform!) dice ! If probability is < than
            mutation_proba then perform mutation.
        2. Select (random uniform) a sequence of genes to inverse
        3. Inverse them
        Parameters
        ----------
        - The offsprings (as a numpy array) on which to apply
            the mutation
        Return
        ------
        - the modified offsprings (althought not necessary as mutation
            is done inplace)
        '''
        rng = np.random.default_rng()
        nb_offsprings = offsprings.shape[0]
        dim = offsprings.shape[1]

        for i in range(nb_offsprings):
            # !!!
            # By ordering the random choice of index, we somehow
            # prevent inversion happening on the array bounds,
            # i.e. inversion on say indexes 8.9.0.1 -> 1.0.9.8
            # will never happen.
            # The effect on the quality of this operator is unknown.
            # In theory, it will be better to also allow these
            # types of inversion, i.e. considering the array as a
            # circular array

            # Probability of performing mutation
            # if < self.mutation_proba perform mutation
            # else NO mutation for this offspring
            if rng.uniform() < self.mutation_proba:
                # Find a sequence of gene to inverse
                invalid_sequence = True
                while invalid_sequence:
                    seq = np.sort(rng.choice(dim, size=2, replace=False))
                    if ((seq[1] - seq[0]) <= self.max_width) and\
                       ((seq[1] - seq[0]) > 1):
                        invalid_sequence = False

                # Inverse the sequence inplace
                offsprings[i][seq[0]:seq[1]] = \
                    offsprings[i][seq[0]:seq[1]][::-1]

        return(offsprings)

    def mutate_x(self, offsprings):
        rng = np.random.default_rng()
        nb_offsprings = offsprings.shape[0]
        dim = offsprings.shape[1]

        for i in range(nb_offsprings):
            # Probability of performing mutation
            # if < self.mutation_proba perform mutation
            # else NO mutation for this offspring
            if rng.uniform() < self.mutation_proba:
                # Find a sequence of gene to inverse
                invalid_sequence = True
                while invalid_sequence:
                    seq = rng.choice(dim, size=2, replace=False)
                    g1 = seq[0]
                    g2 = seq[1]
                    if (abs(g1 - g2) <= self.max_width) and\
                       (abs(g1 - g2) > 1):
                        invalid_sequence = False

                # if gene1 position is > gene2 position, we need
                # to build the sequence to inverse first, that is
                # offspring[g1:] + oggspring[:g2]
                # then inverse it and insert/replace in offspring
                # at the correct position
                if g1 > g2:
                    # Build the reverse sequence
                    seq1 = offsprings[i][g1:]
                    seq2 = offsprings[i][:g2]
                    seq_to_reverse = np.concatenate((seq1, seq2))
                    seq1_size = seq1.shape[0]

                    # insert at the correct position
                    offsprings[i][g1:] = seq_to_reverse[::-1][:seq1_size]
                    offsprings[i][:g2] = seq_to_reverse[::-1][seq1_size:]

                else:
                    # Inverse the sequence inplace
                    offsprings[i][g1:g2] = offsprings[i][g1:g2][::-1]

        return(offsprings)


class Mutation_Scramble:
    '''
    The Scramble (or Shuffle) Mutation operator: A sequence of genes
    is randomly selected and shuffled
    '''
    def __init__(self, mutation_params):
        '''
        Parameters:
        -----------
        - the mutation probability
        - the width of the sequence of genes on which to apply
            shuffling
        '''
        self.mutation_proba = mutation_params["mutation_proba"]
        self.max_width = mutation_params["sequence_max_width"]

    def mutate(self, offsprings):
        '''
        Perform the scramble mutation for all offsprings
        1. roll a (uniform!) dice ! If probability is < than
            mutation_proba then perform mutation.
        2. Select (random uniform) a sequence of genes to scramble
        3. shuffle them
        Parameters
        ----------
        - The offsprings (as a numpy array) on which to apply
            the mutation
        Return
        ------
        - the modified offsprings (althought not necessary as mutation
            is done inplace)
        '''
        rng = np.random.default_rng()
        nb_offsprings = offsprings.shape[0]
        dim = offsprings.shape[1]

        for i in range(nb_offsprings):
            # !!!
            # Similarly to the Mutation Inversion operator,
            # by ordering the random choice of index, we somehow
            # prevent shuffling happening on the array bounds,
            # i.e. shuffling on say indexes 8.9.0.1 -> 9.1.0.8
            # will never happen.
            # The effect on the quality of this operator is unknown.
            # In theory, it will be better to also allow these
            # types of shuffling, i.e. considering the array as a
            # circular array

            # Probability of performing mutation
            # if < self.mutation_proba perform mutation
            # else NO mutation for this offspring
            if rng.uniform() < self.mutation_proba:
                # Find a sequence of gene to shuffle
                invalid_sequence = True
                while invalid_sequence:
                    seq = np.sort(rng.choice(dim, size=2, replace=False))
                    if ((seq[1] - seq[0]) <= self.max_width) and\
                       ((seq[1] - seq[0]) > 1):
                        invalid_sequence = False

                # Shuffle the sequence inplace
                rng.shuffle(offsprings[i][seq[0]:seq[1]])

        return(offsprings)

    def mutate_x(self, offsprings):
        '''
        Perform the scramble mutation for all offsprings
        1. roll a (uniform!) dice ! If probability is < than
            mutation_proba then perform mutation.
        2. Select (random uniform) a sequence of genes to scramble
        3. shuffle them
        Parameters
        ----------
        - The offsprings (as a numpy array) on which to apply
            the mutation
        Return
        ------
        - the modified offsprings (althought not necessary as mutation
            is done inplace)
        '''
        rng = np.random.default_rng()
        nb_offsprings = offsprings.shape[0]
        dim = offsprings.shape[1]

        for i in range(nb_offsprings):
            # !!!
            # Similarly to the Mutation Inversion operator,
            # by ordering the random choice of index, we somehow
            # prevent shuffling happening on the array bounds,
            # i.e. shuffling on say indexes 8.9.0.1 -> 9.1.0.8
            # will never happen.
            # The effect on the quality of this operator is unknown.
            # In theory, it will be better to also allow these
            # types of shuffling, i.e. considering the array as a
            # circular array

            # Probability of performing mutation
            # if < self.mutation_proba perform mutation
            # else NO mutation for this offspring
            if rng.uniform() < self.mutation_proba:
                # Find a sequence of gene to shuffle
                invalid_sequence = True
                while invalid_sequence:
                    seq = np.sort(rng.choice(dim, size=2, replace=False))
                    if ((seq[1] - seq[0]) <= self.max_width) and\
                       ((seq[1] - seq[0]) > 1):
                        invalid_sequence = False

                # Shuffle the sequence inplace
                rng.shuffle(offsprings[i][seq[0]:seq[1]])

        return(offsprings)
