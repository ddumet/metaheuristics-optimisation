# Metaheuristic optimisation
from collins dictionary:

**heuristics**: "*(functioning as singular) mathematics, logic: a method or set of rules for solving problems other than by algorithm*"

**meta-**: "*going beyond or higher*"

**metaheuristic"**: "*first mentionned by Glover, F. in 1986 in his paper on Tabu search: "[Future Paths for Integer Programming and Links to Artificial Intelligence"](https://doi.org/10.1016%2F0305-0548%2886%2990048-1)*.

A metaheuristic is a high-level problem-independent algorithmic framework that provides a set of guidelines or strategies to develop heuristic optimisation algorithms. Examples of metaheuristics include nature-inspired algorithms such as genetic/evolutionary algorithms, simulated annealing or particle swarm optimisation.

All metaheuristic algorithms use a certain tradeoff of randomization and local search. Quality solutions to difficult optimisation problems can be found in a reasonable amount of time with no guarantee to reach the global optimum. Two major components of the metaheuristic algorithms are:
* diversification: generates diverse solutions to explore the search space on a global scale.
* intensification: focus the search on a local region, knowing that a current good solution could be found in this region.

# Metaheuristic problems
This repository contains some of the most standards continuous optimisation problems (e.g. Rosenbrock or Griewank functions) and their resolution using metaheuristics algorithms.

It also contains some discrete optimisation problems, i.e. **Travelling Salesman Problem**.

All these problems can be found (here)[https://github.com/ddumet/metaheuristics-optimisation/tree/master/problems]

# Metaheuristic algorithms
This repository provides some experimental implementation of some of the metaheuristics algorithms. The implementations are based on the book:

 **Meta‐Heuristic and Evolutionary Algorithms for Engineering Optimization.**
 <br>(*Author(s): Omid Bozorg‐Haddad Mohammad Solgi Hugo A. Loáiciga*).

The algorithms implemented so far are:
* Genetic Algorithm
