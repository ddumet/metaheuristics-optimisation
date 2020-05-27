# Shifted Sphere problem
The Shifted Sphere problem is described below as per the **CEC'2008 competition** on large scale global optimisation:

![](shifted-sphere-problem.png)

This problem has only one optimum. We will therefore favor **intensification** over **diversification**.

## Dimension 50
In dimension 50, we use the **Particle Swarm Optimisation GENerational** algorithm (from Pygmo package), with the following configuration:

|config. name|value|
|------------|-----|
|Inertia weight|0.7|
|Social component|0.5|
|cognitive component|4|
|Maximum velocity|0.05|
|Algorithmic variant|FIPS|
|Swarm topology|local best|


