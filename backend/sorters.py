import random
from itertools import groupby


## CUSTOM SHUFFLE FUNCTIONS


# Shuffle with groups
def shuffle_with_groups(ordenadas):
    # Step 1: Sort the list to group identical items together
    sorted_list = sorted(ordenadas, key=lambda x: (x[7][0], x[4], x[5], x[6], x[1], x[2]))
    
    # Step 2: Group the identical items together
    groups = [list(group) for key, group in groupby(sorted_list, key=lambda x: x[7][0])]
    
    # Step 3: Shuffle the groups themselves
    random.shuffle(groups)
    
    # Step 4: Flatten the list of groups
    shuffled_list = [item for group in groups for item in group]
    
    return shuffled_list


# Simple shuffle
def simple_shuffle(ordenadas):
    random.shuffle(ordenadas)
    return ordenadas


# Hierarchies for sorting
jerarquias = [lambda x: (x[7][0], x[4], x[5], x[6], x[1], x[2]), None,
              lambda x: (x[4], x[5], x[6], x[1], x[2]),
              None]