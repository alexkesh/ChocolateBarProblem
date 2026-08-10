import time
import numpy as np

# Import solve functions
from solve1 import solve1
from solve2 import solve2

# Start array (m chocolate bars)
start = [2,5,7]
# Target array (n hungry children)
target = [4,3,2,1]
# Number of times to get repeat execution for average time
n = 10

# Testing getting distinct pairs that add up to elements in start
# NOTE EARLY: this is big loop for large m or s
# for s in start:
#     for i in range(1, s // 2 + 1):
#         print(s,i,s-i)
# exit()

# Execute function n times and average execution time
def exec_timer(func,n):
    # List of times taken
    times = []
    # Initialise check value
    check = 0
    # Loop over avg number
    for i in range(n):
        # Get t0
        t0 = time.perf_counter()
        # Calculate number of cuts
        cuts = solve1(start,target)
        # Get end time
        t1 = time.perf_counter()
        # Calcluate time
        times.append(t1-t0)
        # Check for same answer every time
        if (i == 0):
            # Store value to check against
            check = cuts
        else:
            # If value does not = check value, give critical error
            if (check != cuts):
                raise RuntimeError(f"Critical error: inconsistent cuts — expected {check}, got {cuts}")
    # Get mean time taken
    mean_time = np.mean(times)
    # Return number of cuts and mean time
    return cuts, mean_time


cuts,mean_time = exec_timer(solve1(start,target),n) 
print(f"solve 1 results: number of cuts = {cuts}, avg time take for {n} reps = {mean_time*1e6} us")
cuts,mean_time = exec_timer(solve2(start,target),n) 
print(f"solve 2 results: number of cuts = {cuts}, avg time take for {n} reps = {mean_time*1e6} us")

