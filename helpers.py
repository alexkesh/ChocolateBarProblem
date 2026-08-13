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

# For case where sum(start) < sum(target):
# Proportionally reduce targets while ensuring every child receives at least 1
def reduce_targets(target,start_sum):

    # Number of children
    n = len(target)

    # Cannot give every child at least 1    
    if start_sum < n:
        # For fairness, no child gets any
        raise ValueError("Not enough chocolate to give every child at least 1")

    # Calculate total amount requested
    target_sum = sum(target)

    # No reduction required
    if target_sum <= start_sum:
        return target.copy()

    # Give every child a minimum of 1
    reduced = [1]*n

    # Amount of chocolate remaining after giving everyone 1
    remaining = start_sum-n

    # Calculate chocolate requested above minimum allocation 1
    excess = [t-1 for t in target]

    # Total chocolate requested above the minimum
    excess_sum = sum(excess)

    # Proportionally scale remaining chocolate by demand
    scaled = [e*remaining/excess_sum for e in excess]

    # Round scaled values down so we cannot exceed available chocolate
    allocation = [int(x) for x in scaled]

    # Add these allocations to the minimum of 1
    reduced = [r+a for r,a in zip(reduced,allocation)]

    # Calculate chocolate still available due to rounding down
    remainder = start_sum-sum(reduced)

    # Get indices sorted by largest fractional remainder
    indices = sorted(range(n),key=lambda i: scaled[i]-allocation[i],reverse=True)

    # Distribute remaining chocolate to largest fractional remainders
    for i in indices[:remainder]:
        reduced[i] += 1

    # Return reduced targets
    return reduced
