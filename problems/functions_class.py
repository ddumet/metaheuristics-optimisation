import numpy as np
from functions_cts import BIAS_SPHERE, OPTIMUM_SPHERE
from functions_cts import BIAS_SCHWEFEL, OPTIMUM_SCHWEFEL
from functions_cts import BIAS_ROSENBROCK, OPTIMUM_ROSENBROCK
from functions_cts import BIAS_RASTRIGIN, OPTIMUM_RASTRIGIN
from functions_cts import BIAS_GRIEWANK, OPTIMUM_GRIEWANK
from functions_cts import BIAS_ACKLEY, OPTIMUM_ACKLEY


class Shifted_sphere:
    BIAS = BIAS_SPHERE
    OPTIMUM = OPTIMUM_SPHERE

    def __init__(self, dim):
        self.dim = dim
        if dim > 1000:
            self.dim = 1000
        self.o = self.OPTIMUM[:dim]
        self.o_fitness = -450.0

    def fitness(self, x):
        f = (np.square(x - self.o)).sum() + self.BIAS
        return(f,)

    def get_bounds(self):
        return([-100] * self.dim, [100] * self.dim)

    def get_name(self):
        return("Shifted Sphere Function")

    def get_extra_info(self):
        return("Dimensions: {0}".format(self.dim))


class Shifted_schwefel:
    BIAS = BIAS_SCHWEFEL
    OPTIMUM = OPTIMUM_SCHWEFEL

    def __init__(self, dim):
        self.dim = dim
        if dim > 1000:
            self.dim = 1000
        self.o = self.OPTIMUM[:dim]
        self.o_fitness = -450.0

    def fitness(self, x):
        f = (np.absolute(x - self.o)).max() + self.BIAS
        return(f,)

    def get_bounds(self):
        return([-100] * self.dim, [100] * self.dim)

    def get_name(self):
        return("Shifted Schwefel Function")

    def get_extra_info(self):
        return("Dimensions: {0}".format(self.dim))


class Shifted_rosenbrock:
    BIAS = BIAS_ROSENBROCK
    OPTIMUM = OPTIMUM_ROSENBROCK

    def __init__(self, dim):
        self.dim = dim
        if dim > 1000:
            self.dim = 1000
        self.o = self.OPTIMUM[:dim]
        self.o_fitness = 390.0

    def fitness(self, x):
        z = x - self.o + 1
        f = np.sum((100*np.square(np.square(z[:-1]) - z[1:])
                    + np.square(z[:-1] - 1))) + self.BIAS
        return(f,)

    def get_bounds(self):
        return([-100] * self.dim, [100] * self.dim)

    def get_name(self):
        return("Shifted Rosenbrock Function")

    def get_extra_info(self):
        return("Dimensions: {0}".format(self.dim))


class Shifted_rastrigin:
    BIAS = BIAS_RASTRIGIN
    OPTIMUM = OPTIMUM_RASTRIGIN

    def __init__(self, dim):
        self.dim = dim
        if dim > 1000:
            self.dim = 1000
        self.o = self.OPTIMUM[:dim]
        self.o_fitness = -330.0

    def fitness(self, x):
        z = x - self.o
        f = np.sum((np.square(z) - 10*np.cos(2*np.pi*z) + 10)) + self.BIAS
        return(f,)

    def get_bounds(self):
        return([-5] * self.dim, [5] * self.dim)

    def get_name(self):
        return("Shifted Rastrigin Function")

    def get_extra_info(self):
        return("Dimensions: {0}".format(self.dim))


class Shifted_griewank:
    BIAS = BIAS_GRIEWANK
    OPTIMUM = OPTIMUM_GRIEWANK

    def __init__(self, dim):
        self.dim = dim
        if dim > 1000:
            self.dim = 1000
        self.o = self.OPTIMUM[:dim]
        self.o_fitness = -180.0

    def fitness(self, x):
        z = x - self.o
        sqrt_z_i = np.sqrt(np.arange(1, self.dim+1))
        f = np.sum((np.square(z)/4000)) - np.prod(np.cos(z/sqrt_z_i))\
            + 1 + self.BIAS
        return(f,)

    def get_bounds(self):
        return([-600] * self.dim, [600] * self.dim)

    def get_name(self):
        return("Shifted Griewank Function")

    def get_extra_info(self):
        return("Dimensions: {0}".format(self.dim))


class Shifted_ackley:
    BIAS = BIAS_ACKLEY
    OPTIMUM = OPTIMUM_ACKLEY

    def __init__(self, dim):
        self.dim = dim
        if dim > 1000:
            self.dim = 1000
        self.o = self.OPTIMUM[:dim]
        self.o_fitness = -140.0

    def fitness(self, x):
        z = x - self.o
        f = -20 * np.exp(-0.2*np.sqrt(np.sum(np.square(z))/self.dim))\
            - np.exp(np.sum(np.cos(2*np.pi*z))/self.dim)\
            + 20 + np.e + self.BIAS
        return(f,)

    def get_bounds(self):
        return([-32] * self.dim, [32] * self.dim)

    def get_name(self):
        return("Shifted Ackley Function")

    def get_extra_info(self):
        return("Dimensions: {0}".format(self.dim))
