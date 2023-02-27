# Instances path
INSTANCES_PATH = "data/input/HRTInstances/"
INSTANCES_LIST = [
    217,
    220,
    218,
    221,
    230,
    233,
    242,
    245,
    266,
    231,
    267,
    223,
    226,
    235,
    238,
    250,
    262,
    271,
    274,
    224,
    227,
    236,
    275,
    277,
    313,
    278,
    283,
]
# [x for x in range(217, 337)]

# Max limit of time for exploration per instance
MAX_TIME_LIMIT_SEC = 240

# Fitness
KEEP_UP_TO_CRHOMOSOMES = 1000

# GA learning evolution
INITIAL_PROBABILITY = 0.9
MINIMUM_PROBABILITY = 0.05
EXP_DECAY_FACTOR = 0.95
SIG_K = 0.01  # steepness of the sigmoid
SIG_X0 = 50  # midpoint of the sigmoid

# GA crossover
CROSSOVER_WITH_SORTED_PARENTS = False

# Exploration is MMTSP_SAC, or not
MMTSP_WITH_SAC = True

# Visualisations
# Viridis, Cividis, Bluered, YlGnBu, RdBu, Earth, Jet, Blackbody, Electric, Rainbow, Portland, Magma, Inferno, Plasma, Warm, Cool, Copper
GANTT_COLORMAP = "YlGnBu"
