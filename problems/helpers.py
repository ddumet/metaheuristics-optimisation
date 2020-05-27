from datetime import datetime


import pygmo as pg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm


def pso_gen(problem, population_size, params):
    '''
    Execute the Pygmo PSO_GEN algorithm on an
    optimisation problem with the population size
    and parameters specified. The PSO_GEN possible
    set of parameters are:
    * omega: The inertia weight (or constriction factor,
        depending on the algorithmic variant)
    * eta1: the social component
    * eta2: the cognitive component
    * max_vel: maximum allowed particle velocities
    * variant: algorithmic variant:
            1 -> canonical (with inertia weight)
            2 -> same social and cognitive random
            3 -> same random for all components
            4 -> only one random
            5 -> canonical (with constriction factor)
            6 -> fully informed (FIPS)
    * neighb_type: the swarm topology:
            1 -> gbest (global best)
            2 -> lbest (local best)
            3 -> Von Neumann
            4 -> Adaptative random
    * neighb_param: topology parameter (number of neighbours
            to consider)

    Parameters
    ----------
    - problem: the problem to optimise. It must comply
        to the Pygmo requirements, i.e. being an
        instance of an UDP class
    - population_size: The size of the swarm
    - params: dictionnary of parameters for the
        PSO_GEN algorithm

    Return
    ------
    - log: the logs of the execution of the
        optimisation problem with the population size
    - duration: the total duration of the resolution
        of the  problem
    '''
    # Extract algorithm parameters
    nb_generation = params["nb_generation"]
    omega = params["omega"]
    eta1 = params["eta1"]
    eta2 = params["eta2"]
    max_vel = params["max_vel"]
    variant = params["variant"]
    neighb_type = params["neighb_type"]
    neighb_param = params["neighb_param"]

    algo = pg.algorithm(pg.pso_gen(gen=nb_generation, omega=omega,
                                   eta1=eta1, eta2=eta2, max_vel=max_vel,
                                   variant=variant, neighb_type=neighb_type,
                                   neighb_param=neighb_param, memory=False))
    algo.set_verbosity(1)
    solution = pg.population(problem, size=population_size, b=None)
    startt = datetime.now()
    solution = algo.evolve(solution)
    duration = (datetime.now() - startt)
    uda = algo.extract(pg.pso_gen)
    log = uda.get_log()

    return(log, duration, solution.champion_f, solution.champion_x)


def sade(problem, population_size, params):
    '''
    Execute the Pygmo SADE algorithm on an
    optimisation problem with the population size
    and parameters specified. The SADE possible
    set of parameters are:
    * variant: mutation variant:
            1  -> best/1/exp            10 -> rand/2/bin
            2  -> rand/1/exp            11 -> rand/3/exp
            3  -> rand-to-best/1/exp    12 -> rand/3/bin
            4  -> best/2/exp            13 -> best/3/exp
            5  -> rand/2/exp            14 -> best/3/bin
            6  -> best/1/bin            15 -> rand-to-current/2/exp
            7  -> rand/1/bin            16 -> rand-to-current/2/bin
            8  -> rand-to-best/1/bin    17 -> rand-to-best-and-current/2/exp
            9  -> best/2/bin            18 -> rand-to-best-and-current/2/bin
    * variant_adptv: scale factor F and crossover rate CR
        adaptation scheme to be used
    * ftol: stopping criteria on the function tolerance
    * xtol: stopping criteria on the step tolerance

    Parameters
    ----------
    - problem: the problem to optimise. It must comply
        to the Pygmo requirements, i.e. being an
        instance of an UDP class
    - population_size: The size of the population
    - params: dictionnary of parameters for the
        SADE algorithm

    Return
    ------
    - log: the logs of the execution of the
        optimisation problem with the population size
    - duration: the total duration of the resolution
        of the  problem
    '''
    # Extract algorithm parameters
    nb_generation = params["nb_generation"]
    variant = params["variant"]
    variant_adptv = params["variant_adptv"]
    ftol = params["ftol"]
    xtol = params["xtol"]

    algo = pg.algorithm(pg.sade(gen=nb_generation, variant=variant,
                                variant_adptv=variant_adptv,
                                ftol=ftol, xtol=xtol))
    algo.set_verbosity(1)
    solution = pg.population(problem, size=population_size, b=None)
    startt = datetime.now()
    solution = algo.evolve(solution)
    duration = (datetime.now() - startt)
    uda = algo.extract(pg.sade)
    log = uda.get_log()

    return(log, duration, solution.champion_f, solution.champion_x)


def plot_f_minus_fstar_10(runs, f_optimum, title="title",
                          ylog=True, ylim=None, figsize=(10, 12)):
    '''
    Plot best_fitness = f(fevals) for 10 runs

    Parameters
    ----------
    - logs: A python list: log of 10 runs for
        an optimisation problem. for each run:
        * fevals is run[0]
        * best_fitness is run[1]
        * duration of run is run[2]
        * best ever fitness is run[3]
        * best ever x coordinates is run[4]
    - title: the title of the plot!
    - ylog: True, yscale is log, else linear
    - ylim: zoom on y axis. if None -> [ymin, ymax]
    '''
    # Setting log or linear scale
    if ylog:
        yscale = "log"
    else:
        yscale = "linear"

    # Build the plot
    fig, ax = plt.subplots(figsize=figsize)
    plt.axes(ax)
    plt.yscale(yscale)
    colors = iter(cm.rainbow(np.linspace(0, 1, len(runs))))
    run_id = 0
    for run in runs:
        run_id = run_id + 1
        color = next(colors)
        if run[2].seconds == 0:
            duration = "{0}ms".format(run[2].microseconds//1000)
        else:
            duration = "{0}mn:{1}s".format(run[2].seconds//60,
                                           run[2].seconds % 60)

        # champion_f is a np.array -> [0]
        champion_f = "{0:.9f}".format(run[3][0])

        fevals = np.array(run[0])
        fit_best = np.array(run[1]) - f_optimum
        plt.plot(fevals, fit_best, "k--", color=color,
                 label="run {0:>2}: {1}, champion fit={2}".
                 format(run_id, duration, champion_f))

    # Set y lim if required, title and labels
    if ylim:
        ax.set_ylim(ylim)
    ax.set_title(title)
    ax.set_xlabel("number of function evaluations", fontsize=12)
    ax.set_ylabel("f(x) - f(x*)", fontsize=12)
    ax.legend()


def get_stats(runs, optimum_f, optimum_x):
    '''
    Print main statistics of several runs

    Parameters
    ----------
    - logs: A python list: log of 10 runs for
        an optimisation problem. for each run:
        * fevals is run[0]
        * best_fitness is run[1]
        * duration of run is run[2]
        * best ever fitness is run[3]
        * best ever x coordinates is run[4]
    - optimum_f: the optimum function value
        for this problem
    - optimum_x: the x coordinates of the optimum

    Return
    ------
    The following values for the "best" run,
    defined by the run getting the best fitness
    (champion_f)
    - duration
    - difference with the function's optimum
    - the L2 norm (euclidean distance) to the
        optimum solution
    '''
    best_run_champion_f = np.inf
    for run in runs:
        # run[3] is a np.array
        if run[3][0] < best_run_champion_f:
            best_run_champion_f = run[3][0]
            best_run_duration = run[2]
            best_run_champion_x = run[4]

    diff_optimum = best_run_champion_f - optimum_f
    dimension = best_run_champion_x.shape[0]
    norm2_to_optimum = np.linalg.norm(best_run_champion_x
                                      - optimum_x[:dimension])

    return(best_run_duration, best_run_champion_f,
           diff_optimum, norm2_to_optimum)
