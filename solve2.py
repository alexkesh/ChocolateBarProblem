# ----------------------------------------------------------
# ATTEMPT 2
# Thoughts after second attempt:
# - Major issue here is that for large input, BFS complexity grow exponentially
# - Tests show programmed seemed to hang, but debug below showed queue was not emptying and visited growing
# - Seems to be this is exactly what problem was warning about:
# - "(more interested in solutions that get close to the minimum than that take an exponential amount of time."
# ---------------------------------------------------------- 

from collections import deque

# Testing getting candidates for summing to something actually within target  
# start = [10]
# #target = [3,7,2]
# target = [8]
# for s in start:
#     for i in range(1, s // 2 + 1):
#         print(s,i,s-i)
#     print("--")        
#     candidates = set(t for t in target if 0 < t < s)
#     for i in candidates:
#         print(s,i,s-i)        
#     print("--")        
#     candidates = set(t for t in target if 0 < t <= s // 2)
#     for i in candidates:
#         print(s,i,s-i)
# exit()

# Debug print flag
debug = False

# Solve function 2 - takes start and target as input
def solve2(start,target):

    # Ensure that we have enough chocolate to go around
    if sum(target) > sum(start):
        # Return no solution
        return None
    
    # Initialise number of cuts
    cuts = 0
    
    # Create a queue
    q = deque()

    # Append first node to queue
    q.append((start,target,cuts))

    # Create a set (no duplicates) for visited
    visited = set()
    
    # DEBUG - For debugging apparent hang...
    counter = 0
    
    # Search whole the queue length is non-zerp
    while (len(q) > 0):

        # DEBUG - incrmeent counter
        counter += 1

        # DEBUG - print
        if debug and counter % 5000 == 0:
            print(f"count={counter}, queue={len(q)}, visited={len(visited)}, cuts={cuts}")
        
        # Pop the next node
        start, target, cuts = q.popleft()

        # MOVE THIS TO JUST BEFORE QUEUE PUSH TO STOP DUPLICATES STATES FROM ENTERING THE QUEUE
        # # Create key of this exact situation
        # # Use tuple, sort to ensure e.g. (2,3) and (3,2) are not different states 
        # key = (tuple(sorted(start)),tuple(sorted(target)))

        # # If this key already in the visited set...
        # if key in visited:
        #     # skip
        #     continue
        # # Else, add the key to visited
        # visited.add(key)
        
        # Make a copy of the start (values remaining to find)
        remaining = start.copy()
        # Make a copy of the target
        target = target.copy()

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
        
        # Check if this branch already has no soluton
        if sum(remaining) < sum(target) or max(target) > max(remaining):
            continue

        # Loop through all values remaining to be found
        for i,s in enumerate(remaining):
            # If s value is 1, can safely skip
            if s == 1: continue 
            # Partition each value for every possible pair: in this loop = [j, s-j]
            # possible pairs = candidates for summing to something actually within target
            candidates = set(t for t in target if 0 < t < s)    
            for j in candidates:
                # Create a new node to trial including
                trial_start = remaining[:i] + [j, s-j] + remaining[i+1:]
                # Create key of trial
                # Use tuple, sort to ensure e.g. (2,3) and (3,2) are not different states
                trial_target = target.copy()
                trial_key = (tuple(sorted(trial_start)),tuple(sorted(trial_target)))                
                # If this key already in the visited set...
                if trial_key in visited:
                    # skip
                    continue
                # Else, add the key to visited
                visited.add(trial_key) 
                # Append this node to the queue (incrementing cuts)
                q.append((trial_start,trial_target,cuts+1))

    # No solution
    return None

