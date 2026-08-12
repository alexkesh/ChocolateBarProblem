import random

from solve2 import solve2
from solve3 import solve3
from solve4 import solve4



# Generate a random problem with a known exact minimum number of cuts
def generate_truth_test(m,n,min_target=1,max_target=20):

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
    truth = n - m

    # Return problem and known truth
    return start,target,truth

# Number of random tests
n_tests = 10000

# Number correctly solved
correct = 0

# Loop through random tests
for i in range(n_tests):

    # Random number of starting bars
    m = random.randint(1,10)

    # Random number of targets, ensuring n >= m
    n = random.randint(m,20)

    # Generate random test with known exact solution
    start,target,truth = generate_truth_test(m,n)

    # Solve using solve4
    result = solve4(start.copy(),target.copy())

    # Check against known optimum
    if result == truth:
        correct += 1

# Print accuracy
print(f"Correct = {correct}/{n_tests} ({100*correct/n_tests:.2f}%)")
