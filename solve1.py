# ----------------------------------------------------------
# ATTEMPT 1
# Thoughts after first attempt:
# - Needs to handle no soultion
# - pop(0) is expensive (shifts everything left)
# - Can probably deal with any 1s in the array (skip)
# ---------------------------------------------------------- 

# Solve function 1 - takes start and target as input
def solve1(start,target):

    # Initialise number of cuts
    cuts = 0
    
    # Create a queue
    q = []

    # Append first node to queue
    q.append((start,target,cuts))

    # Search whole the queue length is non-zerp
    while (len(q) > 0):

        # Pop the next node
        start, target, cuts = q.pop(0)

        # Sort the starting array 
        start = sorted(start)

        # Make a copy of the target
        target = target.copy()

        # Make a copy of the start (values remaining to find)
        remaining = start.copy()

        # For every value in start
        for s in start:
            # If that value is in the target 
            if s in target:
                # Remove it from the target
                target.remove(s)
                # And remove it values remaining)
                remaining.remove(s)

        # If we've found every value in the target
        if len(target) == 0:
            #  Return the number of cuts
            return cuts

        # Loop through all values remaining to be found
        for i,s in enumerate(remaining):
            # Partition each value for every possible pair: in this loop = [j, s-j]
            for j in range(1, s // 2 + 1):
                # Create a new node to trial including
                trial = remaining[:i] + [j, s-j] + remaining[i+1:]
                # Append this node to the queue (incrementing cuts)
                q.append((trial,target.copy(),cuts+1))

