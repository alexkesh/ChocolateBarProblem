import random

# Generate a random state with a known exact minimum number of cuts
def gen_states(m,n,min_target=1,max_target=20):

    # Need at least as many targets as starting bars
    if m > n:
        raise ValueError("For this test generator, m must be <= n")

    # Generate n random target values
    target = [random.randint(min_target,max_target) for _ in range(n)]

    # Shuffle target indices so that their allocation to starting bars is random
    indices = list(range(n))
    random.shuffle(indices)

    # Initialise m groups, giving each one target so none are empty
    groups = [[indices[i]] for i in range(m)]

    # Randomly allocate all remaining targets to one of the m groups
    for i in indices[m:]:
        groups[random.randrange(m)].append(i)

    # Construct each starting bar as the sum of the targets in its group
    start = []

    for group in groups:
        start.append(sum(target[i] for i in group))

    # Randomise ordering
    random.shuffle(start)
    random.shuffle(target)

    # Exact minimum number of cuts
    truth = n-m

    # Return problem and known truth
    return start,target,truth
