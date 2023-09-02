def all_overlaps(strings):
    
    """
    Takes list of peptides, returns occurence of overlap of different lengths.
    """
    
    overlaps = []
    for i in range(len(strings) - 1):
        overlaps.append(string_overlap(strings[i], strings[i+1]))

    return Counter(overlaps)