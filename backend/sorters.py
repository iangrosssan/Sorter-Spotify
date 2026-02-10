import random
from itertools import groupby

# Hierarchies for sorting
jerarquias = [lambda x: (x[8][0], x[5], x[6], x[7], x[2], x[3]), None,
              lambda x: (x[5], x[6], x[7], x[2], x[3]),
              None]

# Sort Function
def sort_tracks(l_tracks, jerarquia):
    sorted_tracks = []
    if jerarquia == 1:
        sorted_tracks = shuffle_with_groups(l_tracks)
    elif jerarquia == 3:
        sorted_tracks = simple_shuffle(l_tracks)
    elif jerarquias[jerarquia]:
        key = jerarquias[jerarquia]
        sorted_tracks = sorted(l_tracks, key=key)
    else:
        # Fallback if no hierarchy is selected or invalid
        sorted_tracks = l_tracks

    # DEBUG: Write to CSV
    try:
        with open('backend/o_uri.csv', 'w') as o_uri:
            for i in sorted_tracks:
                o_uri.write(f"{i[0]};")
    except Exception as e:
        print(f"Debug CSV write failed: {e}")

    return sorted_tracks

## CUSTOM SHUFFLE FUNCTIONS

# Shuffle with groups
def shuffle_with_groups(ordenadas):
    # Step 1: Sort the list to group identical items together
    # Assuming index 8 is Artist? Need to verify with original code structure
    # Original: x[8][0] -> Artist name
    # Original: x[5], x[6], x[7] -> Year, Month, Day ?
    # Let's check get_track_data in funciones.py for index mapping
    # 0:uri, 1:name, 2:disc, 3:track, 4:album, 5:year, 6:month, 7:day, 8:artists...
    
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
    # We need a copy to avoid modifying the original list in place if that matters
    shuffled = list(ordenadas)
    random.shuffle(shuffled)
    return shuffled