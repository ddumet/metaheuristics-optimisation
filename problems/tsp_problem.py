import numpy as np
from decimal import localcontext, Decimal, ROUND_HALF_UP


class TSP_Problem:
    '''
    A Travelling Salesman Problem.

    '''
    def __init__(self, problem_name, cities_coords):
        '''
        expecting an array of cities with each
        city's (x,y) coordinate
        cities are numbered from 1 to DIM
        Dimension of the array is therefore (DIM, 2)
        '''
        self.type = "DISCRETE"
        self.dim = cities_coords.shape[0]
        self.lbound, self.ubound = (1, self.dim)
        self.cities_coords = cities_coords
        self.problem_name = problem_name

    def get_distance_int(self, city1, city2):
        '''
        compute the euclidean distance (Norm2)
        between (city1, city2). The result is rounded
        half-up i.e. 2.5 -> 3
        Parameters
        ----------
        - city1, city2: The cities for which to compute
          the distance
        Return
        ------
        - the distance as an int
        '''
        distance = Decimal(np.linalg.norm(city1 - city2))

        # round half up
        with localcontext() as ctx:
            ctx.rounding = ROUND_HALF_UP
            distance = int(distance.to_integral_value())

        return int(distance)

    def get_distance(self, city1, city2):
        '''
        a "float variation" of the computation of the
        euclidean distance (Norm2) between (city1, city2).
        The result is a rounded to 3 decimal places
        Parameters
        ----------
        - city1, city2: The cities for which to compute
          the distance
        Return
        ------
        - the distance as a numpy.float64
        '''
        distance = np.linalg.norm(city1 - city2)

        return round(distance, 3)

    def fitness(self, paths):
        '''
        Compute the fitness of matrix paths.
        Parameters
        ----------
        - paths:  a ndarray of dimension (population_size, dimension)
            containing the different paths (individuals in GA terms!)
            of the current generation
        Return
        ------
        - f:  fitness value(s) vector of dimension (dimension, ),
            representing the fitness of the paths of the current
            generation
        '''

        # a Vector of size (population_size, ) to hold
        # fitness values of the entire population (all paths)
        population_size = paths.shape[0]
        fitness = -1*np.ones(population_size)

        for idx in range(population_size):
            path = paths[idx]

            distance = 0
            for city1, city2 in zip(path, path[1:]):
                # cities in TSP files are numerated from
                # 1 to DIM. However self.cities being indexed
                # starting with 0, coordinate of city number 'i'
                # is at self.cities[i - 1]
                d = self.get_distance_int(self.cities_coords[city1 - 1],
                                          self.cities_coords[city2 - 1])
                distance = distance + d

            # Finally adding the distance back to the first city
            # I.e. distance from path[0] to path[-1]
            d = self.get_distance_int(self.cities_coords[path[0] - 1],
                                      self.cities_coords[path[-1] - 1])
            distance = distance + d
            fitness[idx] = distance

        return(fitness)
