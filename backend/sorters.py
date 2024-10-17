import random
from itertools import groupby



# Sort Function
def sort_tracks(l_tracks, jerarquia):
    open('backend/o_uri.csv', 'w').close()
    if jerarquia == 1:
        l_tracks = shuffle_with_groups(l_tracks)
    elif jerarquia == 3:
        l_tracks = simple_shuffle(l_tracks)
    else:
        key = jerarquias[jerarquia]
        l_tracks.sort(key=key)
    #ordenadas.sort(key=lambda x: (x[7][0], x[4], x[5], x[6], x[1], x[2]))
                                # Artista, año,  mes,  dia, disco, track
    for i in l_tracks:
        with open('backend/o_uri.csv', 'a') as o_uri:
            o_uri.write(f"{i[0]};")
    return l_tracks

## CUSTOM SHUFFLE FUNCTIONS

# Shuffle with groups
def shuffle_with_groups(ordenadas):
    # Step 1: Sort the list to group identical items together
    sorted_list = sorted(ordenadas, key=lambda x: (x[8][0], x[5], x[6], x[7], x[2], x[3]))
    
    # Step 2: Group the identical items together
    groups = [list(group) for key, group in groupby(sorted_list, key=lambda x: x[8][0])]
    
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
jerarquias = [lambda x: (x[8][0], x[5], x[6], x[7], x[2], x[3]), None,
              lambda x: (x[5], x[6], x[7], x[2], x[3]),
              None]