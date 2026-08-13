import time
import numpy as np

# Import solve functions
from solve1 import solve1
from solve2 import solve2
from solve3 import solve3
from solve4 import solve4

# Test arrays
states = [
    [[6],[6]], # No cuts needed
    [[2, 5],[4, 3, 2, 1]], # Check sum(start) < sum(target)
    [[3,3],[6]], # Check that a child can be given several smaller pieces from different bars (Jake, 11/08/26)
    [[2, 5, 7],[4, 3, 2, 1]], # Provided example
    [[10, 15],[5, 5, 10, 5]], # Matching sum
    [[1, 7, 7, 8],[3, 3, 6]], 
    [[4, 4],[3, 3, 2]], 
    [[50, 30, 20],[10, 10, 10, 10, 10, 10, 10, 10, 10,10]], # Large matching sum, lots of children, all duplicates
    [[23, 47, 31, 19, 12],[5, 7, 3, 9, 11, 13, 17, 2, 4, 6, 8, 10]] # Very large inputs
]                

# Number of times to get repeat execution for average time
n = 100

# Execute function n times and average execution time
def exec_timer(func,start,target,n):
    # List of times taken
    times = []
    # Initialise check value
    check = 0
    # Loop over avg number
    for i in range(n):
        # Get t0
        t0 = time.perf_counter()
        # Calculate number of cuts
        cuts = func(start,target)
        # Get end time
        t1 = time.perf_counter()
        # Calculate time
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

    # Return number of cuts, mean time and maximum time
    return cuts, mean_time, max(times)

for start,target in states:
    print(f"start = {start}, target = {target}")
    # cuts,mean_time = exec_timer(solve1(start,target),n) 
    # print(f"solve 1 results: number of cuts = {cuts}, avg time take for {n} reps = {mean_time*1e6} us")
    # cuts,mean_time = exec_timer(solve2(start,target),n) 
    # print(f"solve 2 results: number of cuts = {cuts}, avg time take for {n} reps = {mean_time*1e6} us")
    cuts,mean_time,max_time = exec_timer(solve3,start,target,n) 
    print(f"\tsolve 3 results: number of cuts = {cuts}, avg time take for {n} reps = {mean_time*1e6:.4f} us, max time = {max_time*1e6:.4f} us")
    result,mean_time,max_time = exec_timer(solve4,start,target,n)
    print(f"\tsolve 4 results: {result}")
    print(f"\t                 avg time take for {n} reps = {mean_time*1e6:.4f} us, max time = {max_time*1e6:.4f} us")

