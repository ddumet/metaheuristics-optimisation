import numpy as np
from genalg import genalg


def rosenbroke_func(x):
    # we return -rosenbroke_func(x) as Genetic Algorithm is a maximisation
    # algorithm and we're looking for min(rosenbroke_func)

    # The rosenbroke function has exactly one minimum for
    # dimension=3 at x = (1,1,1) and exactly two minima for
    # dimension [4,7]

    r = -sum(100*np.square((x[1:] - np.square(x[:-1]))) + np.square(x[:-1]-1))

    return r


ga = genalg(rosenbroke_func,
            dims=3,
            rparents=0.5,
            popsize=100,
            pcrossover=0.5,
            pmutate=0.5,
            s_gen=300)

ga.run(verbose=True)
