# ----------------------------------------------------------
# ATTEMPT 3
# Thoughts before third attempt:
# - Need to try and find some approximate solution that does have exponential complexity growth
# - Go back to first idea --> matching target to start
# - Can a reverse search (something like a two-sum when I match target to start) help?
# - Idea: approximate by finding chocolcate bar lengths that most match target sizes...
# Thoughts after third attempt:
# - The implementation gives an approximate solultion, but avoids exponential time
# - Iteratively finds a locally best choice, instead of the globally best one.
# - Answers seem to be correct for less complicated cases.
# - Thoughts to improve further: weight search towards matching target/pair/more that sum to one bar. 
# ***************************** 
# NOTE: Received Jake's reply on 11/08/26 to questions about assumptions/constraints.
# In all solutions thus far (including solve3) I had assumed based on the provided example that
# a child's amount should come from a single piece. This is NOT a requirement!
# To reach a target value, a child can be given several smaller pieces, and those can come from different bars.
# This reframes the problem, and requires a new solution...
# For example, start = [3,3] and target = [6] returns None here.
# (All other implemented assumptions and constraints correct)
# *****************************
# 
# ---------------------------------------------------------- 

# Solve function 3 - takes start and target as input
def solve3(start, target):

    # Ensure that we have enough chocolate to go around
    if sum(target) > sum(start):
        # Return no solution
        return None

    # Remaining chocolate bars
    remaining = start.copy()

    # Initialise arrays to keep track of which children use each bar
    assigned = [[] for _ in start]

    # Loop through all target pieces of chocolate from largest to small
    for t in sorted(target, reverse=True):

        # Find every back this child's piece can come from
        possible = []

        # Loop through all remaining chocolate bars
        for i, r in enumerate(remaining):
            # If the target size is within the bar size
            if t <= r:
                # Possible match of target to start
                possible.append(i)

        # If no possible matches...
        if len(possible) == 0:
            # No solution
            return None

        # Find index i in possible that minimises remaining[i] - t (smallest leftover chocolate)
        best = min(
            possible,
            key=lambda i: remaining[i] - t
        )

        # Assign this child chocolate from that bar
        assigned[best].append(t)

        # Remove the child's amount from that bar
        remaining[best] -= t

    # Initialise number of cuts
    cuts = 0

    # Loop through all chocolate bars
    for i in range(len(start)):

        # Get the children assigned to this chocolate bar
        children = assigned[i]

        # If no children assigned to this chocolate bar
        if len(children) == 0:
            # Skip
            continue
        
        # If the entire bar has been used
        if remaining[i] == 0:
            # Number of cuts in this bar= number of children - 1: e.g. 1 bar, 2 children, no remainder = 1 cut
            cuts += len(children) - 1
        # Else if there is some chocolcate remaining in this bar
        else:
            # Number of cuts in this bar = number of children: e.g. 1 bar, 2 children, with remainder = 2 cuts
            cuts += len(children)

    # Reutrn number of cuts            
    return cuts
