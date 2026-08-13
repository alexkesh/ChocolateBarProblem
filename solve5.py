# ----------------------------------------------------------
# - Global solution, exponential time, with correct assumptions
# - Adapting pprevious BFS implementation (solve2)
# - Implementing for time/accuracy reference against solve4 with same assumptions
# - Previously assumed that each child's target amount had to come from a single piece.
# - Jake clarified on 11/08/26 that this is NOT a requirement:
#   a child can receive several smaller pieces, potentially from different chocolate bars.
# Thoughts before implementing solve5
# - Want to merge the solve2 with assumptions and lessons learned from solve4.
# - E.g. use reduce_targets() if sum(target) > sum(start) and return format consistent with solve4
# - Consider different states: whole piece to a child = 0 cuts, splitting a piece = 1 cut.
# Thoughts during/after implementing solve 5:
# - Need to deal with 0 cut allocations - push to front of queue, not back!
# - Replace visited set used in solve2 with best dictionary storing the
#   minimum number of cuts with which each state has been reached.
# ----------------------------------------------------------

from collections import deque

from helpers import reduce_targets

# Solve function 5 - exact search allowing children to receive multiple pieces
def solve5(start,target):

    # Not enough chocolate 
    exact_target = True
    adjusted_target = target.copy()
    if sum(target) > sum(start):
        adjusted_target = reduce_targets(target, sum(start))
        exact_target = False

    # Work with the adjusted target
    target = adjusted_target.copy()

    # Sort initial state
    start = sorted(start)
    target = sorted(target)

    # Create a queue
    q = deque()

    # Append first node to queue
    q.append((start,target,0))

    # Best dictionary = minimum cuts with which each state has been reached
    best = {}

    # Create key of initial state
    key = (tuple(start),tuple(target))

    # Initial state requires zero cuts
    best[key] = 0

    # Search while the queue length is non-zero
    while (len(q) > 0):

        # Pop the next node
        start, target, cuts = q.popleft()

        # If we've found every value in the target
        if len(target) == 0:
            # Return result
            return {"cuts": cuts,"exact_target": exact_target,"target_used": adjusted_target}

        # Loop through all remaining pieces
        for i,s in enumerate(start):
            # Loop through all remaining child requirements
            for j,t in enumerate(target):

                # 1) Give this entire piece to this child (no cut is required)

                # If chocolate piece is <= than target piece
                if s <= t:
                    # Remove this piece from start
                    trial_start = start[:i] + start[i+1:]
                    # Make a copy of target
                    trial_target = target.copy()
                    # If this exactly satisfies the child
                    if s == t:
                        # Remove this child from target
                        trial_target.pop(j)
                    # Otherwise reduce this child's remaining requirement
                    else:
                        # Reduce remaining requirement
                        trial_target[j] -= s
                    # Sort to make equivalent states identical
                    trial_start = sorted(trial_start)
                    trial_target = sorted(trial_target)
                    # Create key of trial
                    trial_key = (tuple(trial_start),tuple(trial_target))
                    # If we have not reached this state before with
                    # an equal or smaller number of cuts
                    if trial_key not in best or cuts < best[trial_key]:
                        # Record the number of cuts
                        best[trial_key] = cuts
                        # No cut was made, so put at front of queue
                        q.appendleft((trial_start,trial_target,cuts))


                # 2) Piece is larger than the child's remaining requirement

                # If chocolate piece is < than target piece
                else:
                    # Amount remaining after cutting off target
                    remainder = s - t
                    # Replace original piece with remainder
                    trial_start = (start[:i] + [remainder] + start[i+1:])
                    # This child is completely satisfied
                    trial_target = (target[:j] + target[j+1:])
                    # Sort to make equivalent states identical
                    trial_start = sorted(trial_start)
                    trial_target = sorted(trial_target)
                    # One additional cut
                    trial_cuts = cuts + 1
                    # Create key of trial
                    trial_key = (tuple(trial_start),tuple(trial_target))
                    # If we have not reached this state before with
                    # an equal or smaller number of cuts
                    if trial_key not in best or trial_cuts < best[trial_key]:
                        # Record the number of cuts
                        best[trial_key] = trial_cuts
                        # One cut was made, so put at back of queue
                        q.append((trial_start,trial_target,trial_cuts))

    # With the target reduction above, a solution should always exist
    raise RuntimeError("solve5 failed to find a solution")                        

