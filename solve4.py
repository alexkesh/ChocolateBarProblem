# ----------------------------------A-----------A-------------
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

from helpers import *

# Solve function 4 - takes start and target as input
def solve4(start, target):

    # Calculate totals
    start_sum = sum(start)
    target_sum = sum(target)

    # Not enough chocolate
    exact_target = True
    adjusted_target = target.copy()  
    if target_sum > start_sum:
        adjusted_target = reduce_targets(target,start_sum)
        exact_target = False
        
    # Copy start and target
    start = start.copy()
    target = adjusted_target.copy()

    # Initialise number of cuts
    cuts = 0

    # # Add dummy target for unused chocolate
    # NOTE - DUMMY ADDED TO 3) ONLY!
    # if start_sum > target_sum:
    #     target.append(start_sum - target_sum)

    # Continue while there are still targets
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
        # Here, calculate and inlcude dummy target for currently unused chocolate
        dummy = sum(start) - sum(target)
        # Copy target to temporarily include dummy
        target_with_dummy = target.copy()
        # If there is going to be unused chocolate
        if dummy > 0:
            # Add dummy to temporary target
            target_with_dummy.append(dummy)
        # Look for a two-sum including dummy (where the dummy can satisfy the two-sum)
        match = two_sum(target_with_dummy, start)
        # If a two-sum has been found
        if match is not None:
            # Get two-sum match indices
            i, j, k = match
            # Remove start
            start.pop(k)
            # Remove corresponding two targets
            for index in sorted((i, j), reverse=True):
                # Only remove if this is a real target (not dummy)
                if index < len(target):
                    target.pop(index)
            # Increment number of cuts by 1
            cuts += 1
            # State-change: go back to step 1)
            continue

        # 4) Approximate remaining chocolate distribution from large to small
        # Local optimisation - not global solution

        # Find the index of the largest remaining target
        t_index = max(range(len(target)),key=lambda i: target[i])
        # Find the value of the largest remaining target
        t = target[t_index]

        # 4.a) First preference: 0  cuts.
        # Find all the indices of all values in start less than the largest target
        candidates = [i for i, s in enumerate(start) if s < t]
        # If they exist...
        if candidates:
            # Find the index in candidates that corresponds to the largest value in start
            i = max(candidates,key=lambda i: start[i])
            # Give the whole bar to this child. Remove from start.
            s = start.pop(i)
            # The child still needs t - s.
            target[t_index] -= s
            # State-change: go back to step 1) 
            continue

        # --------------------------------------------------
        # 4.b) Second preference: 1 cut.
        # Find the smallest bar larger than target and cut
        # exactly what we need from it.
        # Find all the indices of all values in start larger than the largest target 
        candidates = [i for i, s in enumerate(start) if s > t]
        # If they exist...
        if candidates:
            # Find the index in candidates that corresponds to the smallest value in start
            i = min(candidates,key=lambda i: start[i])
            # Cut target amount from bar, leaving the remainder
            start[i] -= t            
            # Remove from target. This child is now completely satisfied.
            target.pop(t_index)
            # One cut
            cuts += 1
            # State-change: go back to step 1) 
            continue

        # This shouldn't be reached
        raise RuntimeError(
            "Solve4 reached impossible state. "
            f"start={start}, target={target}, dummy={dummy}"
        )

    return {"cuts": cuts,"exact_target": exact_target,"target_used": adjusted_target}
