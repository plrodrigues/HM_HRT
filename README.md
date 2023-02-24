# Heuristics and Metaheuristics Project

Scheduling Human-Robot Teams in collaborative working cells


## Run the project

```bash
```

## Project Tasks

1. Build function to read instances information from text files
2. Build search space
3. Code restrictions
4. Code Genetic Algorithm solution for this problem
5. Read the results and compare with Lower Bound

## Problem Definition

Inspired by [Ferreira C., Figueira G., Amorim P. "Scheduling human-robot teams in collaborative working cells" Int. J. Prod. Econ., 235 (2021), Article 108094](https://www.sciencedirect.com/science/article/abs/pii/S0925527321000700)

Type of Multimode Multiprocessor Task Scheduling Problem (MMTSP).

- Non-identical resources $R$
- Set of jobs $J$
- A mode $m$ is composed of a subset of resources $R_m$ such that $Rm \subseteq R$
- A job $j$ must be executed in one of the possible modes $M_j$, each requiring a specific processing time $p_{jm}$
- Each resource only processes one job at a time

Additionally, within MMTSP detininion:

- A set of jobs $J$ is divided into working spaces.
- Each working space $w=\{1, ..., n\}$ is responsible for a single piece per cycle, which requires a set of jobs $J_m \subset J$ (Each working space can only process one job piece at a time.)
- Each job $j \in J_w$ has $n$ replications (one in each working space)
  - Each main job is a sequence of jobs in the instances.txt (let's call them **task**). We can find the different main jobs, by analysing what's the job in the txt that has no precence. These will be the first tasks of each main job.
  - The duration each job task takes per resource is the same between working spaces
  - The precedence of jobs tasks is the same in all jobs in instances.

MMTSP-SAC (Symmetric Assignment Constraints (SAC)):

- Jobs in $J_w$ must be assigned to resources from $HRT_w$
- The assignment of jobs to modes must be the same for all their replications.

Mixed integer programming formulation (MIP) for the MMTSP:

- $Y_{jm}$ - binary variable if job $j$ is assigned to model $m$
- $S_{jm}$ - starting time of job $j$ in mode $m$
- $F_{jm}$ - ending time of job $j$ in mode $m$

*If this mode is not selected, those variables take the value 0.*

- $X_{rij}$ - indicates that job $i$ precedes job $j$ in resource $r$ *(this assumes that both jobs $i$ and $j$ are assigned to modes tht contain resource $r$)*

Precedence constraints:

- $A = \{(i, j) : i, j \in J, i \prec j\}$ - i.e. the set of all pairs of jobs where job $i$ must be executed before job $j$.
- $M_{jr} = \{m \in M_j: r \in R_m\}$ - i.e. the subset of modes of job $j$ that contain resource $r$.

The objective is to **minimise the makespan given by C**:

- $H$ is an upper bound for $C$, calculated as $\sum_{j \in J}\hat{p}_j$, where $\hat{p}_j = max_{m \in M_j}p_{jm} \forall j \in J$

### The model

- $Min \ C \ \Longrightarrow$ minimise the total makespan of the Job in the instance.

- $\sum_{m \in M_j} Y_{jm} = 1 \ \forall j \in J \ \Longrightarrow$ ensure that each job is assigned to one and only one mode.

- $F_{jm} >= S_{jm} + p_{jm} + H \cdot (Y_{jm} - 1) \ \forall j \in J, \forall m \in M_j \ \Longrightarrow$ calculate the ending time of each job, according to its assignment.

- $S_{jm} >= F_{im'} + H \cdot (Y_{jm} - 1) \ \forall (i, j) \in A, \forall m \in M, \forall m' \in M_i \ \Longrightarrow$ stablish the pre-defined precendence relations.

- $S_{jm} >= F_{im'} + H \cdot (Y_{jm} + Y_{im'} + X_{rij} - 3) \ \forall i, j \in J, \forall r \in R, \forall m \in M_{jr}, \forall m' \in M_{ir}\ \Longrightarrow$ (A)
- $S_{im} >= F_{jm} + H \cdot (Y_{jm} + Y_{im'} + X_{rij} - 2) \ \forall i, j \in J, \forall r \in R, \forall m \in M_{jr}, \forall m' \in M_{ir} \ \Longrightarrow$ (B)

  - (A) and (B) ensure that each resource will not provess more than one job at a time ('no-overlap').

- $C >= F_{jm} \ \forall i \in J, \forall m \in M_j \ \Longrightarrow$ calculate the makespan

- $Y_{jm} \in \{0, 1\} \ \forall i \in J, \forall m \in M_j \ \Longrightarrow$ (C)
- $X_{rij} \in \{0, 1\} \ \forall i \in J, \forall r \in R \ \Longrightarrow$ (D)
  - (C) and (D) define the domain of the variables.

- $X_{j_1 m} = X_{j_w m} \ \forall i_1 \in J_1, \forall m \in M_j, \forall w \in \{2, ..., n\} \ \Longrightarrow$ given that $j_1$ belongs to $J_1$, and $j_w$ is the replication of $j_1$ in working space $J_w$.



