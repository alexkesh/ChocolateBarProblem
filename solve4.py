# ---------------------------------------------A-------------
# ATTEMPT 4
# ***************************** 
# To reach a target value, a child can be given several smaller pieces, and those can come from different bars.
# This reframes the problem, and requires a new solution...
# (All other implemented assumptions and constraints correct)
# ***************************** 
# Thoughts before fourth attempt:
# - With this flexibility, tthere is ALWAYS a solution if sum(start) >= sum(target).
# - There is only no solution is sum(start) < sum(target). This is already handled with return None.
# - Can it instead be handled by feeding an approximation of the target with minimum cuts...?
# - Trial matching targets to start values, by order of number of cuts (up to some cap)
# - Then default back to solve3
# Thoughts after fourth attempt:
# - 
# ---------------------------------------------------------- 

# Remove any exact matches
def remove_exact_matches(start, target):

    # Dictionary of how many times each value appears in target
    target_counts = {}

    # Loop through target
    for t in target:
        # If this value already exists in the dictionary
        if t in target_counts:
            # Increase its count
            target_counts[t] += 1
        else:
            # Else, add to dictionary
            target_counts[t] = 1

    # Initliase new start array (to contain unmatched values)
    new_start = []

    # Loop through start
    for s in start:
        # If there is an unused target exactly matching s
        if s in target_counts and target_counts[s] > 0:
            # Decrement the amount of times it appears in the target
            target_counts[s] -= 1
        # Otherwise, keep in start
        else:
            new_start.append(s)

    # Initliase new target array (to contain unmatched values)
    new_target = []

    # Create new unmatched target array based on remaining counts
    for t, count in target_counts.items():
        new_target.extend([t] * count)

    # Return unmatched start and target
    return new_start, new_target

# Two-sum algorithm to look for: values[i] + values[j] = targets[k]
def two_sum(values, targets):

    # Loop through all two-sum targets
    for k, target in enumerate(targets):
        # Initiliase dictionary of seen values
        seen = {}
        # Loop through all values to be summer
        for j, value in enumerate(values):
            # Find the difference value we hope to find
            needed = target - value
            # If that difference is in the seen values
            if needed in seen:
                # Return the indices of the found two-sum
                return seen[needed], j, k
            # Add to dictionary of seen values
            seen[value] = j
    # No two-sum found
    return None

# Solve function 4 - takes start and target as input
def solve4(start, target):

    # Copy start and target
    start = start.copy()
    target = target.copy()

    # Initialise number of cuts
    cuts = 0

    # Calculate totals
    start_sum = sum(start)
    target_sum = sum(target)

    # Not enough chocolate
    if target_sum > start_sum:
        return None

    # Add dummy target for unused chocolate
    if start_sum > target_sum:
        target.append(start_sum - target_sum)

    # Continue while there are still targets (including dummy)
    while target:

        # 1) Look for and remove any exact matches between start and target (0 cuts)
        start, target = remove_exact_matches(start, target)
        # If exact match was last target
        if not target:
            break

        # 2) Look for the 0 cut case of two starts = one target
        match = two_sum(start, target)
        # If a two-sum has been found
        if match is not None:
            # Get two-sum match indices
            i, j, k = match
            # Remove the two starts
            for index in sorted((i, j), reverse=True): start.pop(index)
            # Remove corresponding target
            target.pop(k)
            # State-change: go back to step 1)
            continue

        # 3) Look for the 1 cut case of one start = two targets
        match = two_sum(target, start)
        # If a two-sum has been found
        if match is not None:
            # Get two-sum match indices
            i, j, k = match
            # Remove start
            start.pop(k)
            # Remove corresponding two targets
            for index in sorted((i, j), reverse=True): target.pop(index)
            # Increment number of cuts by 1
            cuts += 1
            # State-change: go back to step 1)
            continue

        # 4) Choose the largest remaining target
        t_index = max(range(len(target)),key=lambda i: target[i])
        t = target[t_index]

        # 4.a) First preference: 0  cuts.
        candidates = [i for i, s in enumerate(start) if s < t]
        if candidates:
            # Choose the largest bar which fits
            i = max(candidates,key=lambda i: start[i])
            # Remove from start
            s = start.pop(i)
            # Give the whole bar to this child.
            # The child still needs t - s.
            target[t_index] -= s
            # State-change: go back to step 1) 
            continue

        # --------------------------------------------------
        # 4.b) Second preference: 1 cut.
        # Find the smallest bar larger than target and cut
        # exactly what we need from it.
        candidates = [i for i, s in enumerate(start) if s > t]
        if candidates:
            # Best fit: smallest bar large enough
            i = min(candidates,key=lambda i: start[i])
            # Remove from start
            s = start.pop(i)
            # Amount left after cutting off target
            remainder = s - t
            # Remove from target
            # This target is now completely satisfied
            target.pop(t_index)
            # Put unused part of bar back into start
            start.append(remainder)
            # One cut
            cuts += 1
            # State-change: go back to step 1) 
            continue


        # With balanced positive integer inputs this
        # shouldn't be reached
        return None

    return cuts
