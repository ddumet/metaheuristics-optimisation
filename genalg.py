import numpy as np
from secrets import SystemRandom, randbelow, choice
from itertools import combinations


class state:
    '''
    Store some keys components of the algorithm's
    results at each generation:
        generation: the generation number
        best_x:     the best solution
        best_y:     the optimal value found

    This information could be used, e.g. for printing
    convergence curve.

    '''

    def __init__(self):
        self.generation = []
        self.best_x = []
        self.best_y = []

    def add(self, g, x, y):
        self.generation.append(g)
        self.best_x.append(x)
        self.best_y.append(y)


class genalg:

    def __init__(self, func, dims=None,
                 popsize=None, rparents=0.3, minparents=2,
                 pcrossover=0.5, pmutate=0.4,
                 lower=-10, upper=10, s_gen=50):
        '''
        Parameters for __init__ function
            func:       objective function (to maximise)
            dims:       dimension of the problem, i.e. the number
                        of the decision variables
            popsize:    population size
            rparents:   ratio of parents to be retained for the next
                        generation ([0,1])
            minparents  minimum number of parents to be selected
                        for reproduction (avoiding having a single parent
                        when population size and parents ratio being low)
            pcrossover  crossover probability
            pmutate     mutation probability
            lower       lower bound of the space search
            upper       upper bound of the space search
            s_gen       stop condition: Algorithm stops after 's_gen'
                        generation have been created

        '''

        if dims is None:
            raise ValueError("parameter 'dims' cannot be null")

        # GA general parameters
        # fitness function
        self.func = func

        # number of decision variable
        self.dims = dims

        # population size
        # if not set, we set a default value of dims * 4
        if popsize is None:
            popsize = dims * 4
        self.popsize = popsize

        # lower bound of the decision variables
        self.lower = lower

        # Upper bound of the decision variables
        self.upper = upper

        # [0,1] ratio of parents to select for reproduction
        self.rparents = rparents

        # number of parent to select for reproduction
        self.nb_rp = int(round(self.popsize*self.rparents))

        # Crossover probability
        self.pc = pcrossover

        # minimum number of parents for crossover
        # required as probabilistic selection using
        # crossover probability only could end up with
        # empty set !
        # we required at least TWO parents
        if minparents < 2:
            minparents = 2
        self.minparents = minparents

        # Gene mutation probability
        self.pm = pmutate

        # STOP condition
        # stopping after s_gen generation
        self.s_gen = s_gen

        # Main GA class attributes
        # current population
        self.pop = None

        # selected parents for crossover
        self.parents = None

        # selected parents for crossover
        self.offsprings = None

        # Save state at each generation
        self.state = state()

    def init_population(self):
        '''
            initialise 'self.pop' to a np.array of
            dimension = (pop_size, dimension)

        '''

        self.pop = np.random.uniform(self.lower,
                                     self.upper,
                                     (self.popsize, self.dims))

    def pop_fitness(self):
        '''
        Simply compute the fitness function

        '''

        return self.func(self.pop.transpose())

    def select(self):
        '''
        Parents selection

        Select the parents solution to be retained for REPRODUCTION step.
        Different methods could be used:
        - Proportionate selection
        - Ranking selection
        - Tournament selection

        Notes
        -----
        Only method implemented here is Proportionate selection

        To Do
        -----
        Implement each selection method (preferably as different function,
        or a separate class)

        '''

        # Matrix of population fitness values dim=(p_size)
        pop_fval = self.pop_fitness()

        # Probability of Kth solution
        sum_fval = np.sum(pop_fval)
        pk = pop_fval/sum_fval

        # Cumulative distribution of Jth solution
        qj_list = [np.sum(pk[:j]) for j in range(1, self.popsize+1)]

        # we store the INDEX of the parents to retain
        rp_idx = []
        while 1:
            rn = SystemRandom.random(1)

            # if an empty list is returned, the parent
            # to select is first one in cumulative distribution
            p = [i for i in qj_list if i <= rn]
            if len(p) == 0:
                p = 0

            # else the parent to select is the last
            # item in the "p" list
            else:
                p = p.index(p[-1])

            # verify the parent has not already be selected
            # (else do nothing!)
            if p not in rp_idx:
                rp_idx.append(p)

        # !!!!!!!!!!!!!!
        # Fuzzy here ...
        # Number of parents to retain for next generation
        # could be (is ??) different from the number of
        # parents used for reproduction
        # !!!!!!!!!!!!!!

            # break loop if number of parent to retain has been reached
            if len(rp_idx) == self.nb_rp:
                break

        # !!!!!!!!!!!!!!
        # Should we keep oly the idx here
        # instead of re-creating an array?
        # i.e. can be recreated at anytime from self.pop
        # !!!!!!!!!!!!!

        self.parents = self.pop[rp_idx]

    def crossover(self):
        '''
        Perform crossover

        Crossover consists in selecting pairwise parents to generate children.
        It happens in several steps:
        1) Select effective parents according to a general parameter pc
            (crossover probability)
        2) loop over the number of offspring to generate
           ((population size - nb of parents to retain for next gen) / 2)
        3) at each iteration generate two offsprings by crossing-over
           parents' genes.
           One point crossover is used here.

        To Do
        -----
        Implement each crossover method (preferably as different function,
        or a separate class)

        '''

        # Select parents for reproduction
        # ('efficient' parent ep)
        ep_idx = []

        while 1:
            for i in range(0, self.parents.shape[0]):
                if SystemRandom.random(1) < self.pc:
                    # effective parent (select for reproduction)
                    ep_idx.append(i)

            # making sure we do not have duplicated parents
            ep_idx = list(dict.fromkeys(ep_idx))

            # we want at least self.minparents parents
            if len(ep_idx) > (self.minparents - 1):
                break

        # combinations of effective couples for reproduction
        couples = list(combinations(ep_idx, 2))

        # generate children
        # select a couple and crossover parents
        # at crossover point

        # number of offsprings to generate
        # (population size - nb of parents) / 2
        nb_o = int(round((self.popsize - self.parents.shape[0])/2))

        # Crossover
        # Using one point crossover
        offsprings = np.empty([0, self.dims])

        for i in range(0, nb_o):
            # select two parents as base for offsprings
            couple = choice(couples)

            # select crossover point
            c = randbelow(self.dims+1)

            os1 = np.append(self.parents[couple[0]][:c],
                            self.parents[couple[1]][c:])
            offsprings = np.vstack((offsprings, os1))

            os2 = np.append(self.parents[couple[1]][:c],
                            self.parents[couple[0]][c:])
            offsprings = np.vstack((offsprings, os2))

        self.offsprings = offsprings

    def mutate(self):
        '''
        Perform mutation of offsprings

        Mutation of genes of each offspring given the mutation probability.
        Uniform mutation is used here (generating new genes within the
        feasible space)

        To Do
        -----
        Implement non-uniform mutation.

        '''

        # loop through all offsprings
        for offspring in self.offsprings:

            # generate 'dims' random number and create a mask
            rns = np.random.rand(self.dims)
            mask = rns < self.pm

            # create as many new genes as needed
            # (new genes needed are sum(mask), i.e. sum(True))
            # genes are created within the feasible solution
            offspring[mask] = np.random.uniform(self.lower,
                                                self.upper, (np.sum(mask)))

    def run(self, verbose=False):
        '''
        Run !
        Which consists in:
        * initialising the population
        * iterating on 's_gen' (stop condition on number of generation)
            - perform selection
            - perform crossover
            - perform mutation

        '''

        self.init_population()

        for i in range(0, self.s_gen):
            self.select()
            self.crossover()
            self.mutate()

            # Adding best parents (parents with best fitness)
            # to this new generation
            rp_idx = np.argsort(self.pop_fitness())[-self.nb_rp:]

            best_fitness_idx = np.argsort(self.pop_fitness())[-1]
            best_fitness = self.pop_fitness()[best_fitness_idx]
            best_x = self.pop[best_fitness_idx]

            # updating the new generation (population)
            # with retained parents and new offsprings
            self.pop = self.pop[rp_idx]
            self.pop = np.vstack((self.pop, self.offsprings))

            self.state.add(i, best_x, -best_fitness)

        if verbose:
            print("best solution: {0}".format(self.state.best_x[-1]))
            print("optimum value: {0}".format(self.state.best_y[-1]))
