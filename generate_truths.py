import random
import matplotlib.pyplot as plt

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

# # Generate a random problem with a known exact minimum number of cuts
# def generate_truth_test(m,n,min_target=1,max_target=20):

#     # Need at least as many targets as starting bars
#     if m > n:
#         raise ValueError("For this test generator, m must be <= n")

#     # Generate n random target values
#     target = [random.randint(min_target,max_target) for _ in range(n)]

#     # Shuffle target indices so that their allocation to starting bars is random
#     indices = list(range(n))
#     random.shuffle(indices)

#     # Initialise m groups, giving each one target so none are empty
#     groups = [[indices[i]] for i in range(m)]

#     # Randomly allocate all remaining targets to one of the m groups
#     for i in indices[m:]:
#         groups[random.randrange(m)].append(i)

#     # Construct each starting bar as the sum of the targets in its group
#     start = []

#     for group in groups:
#         start.append(sum(target[i] for i in group))

#     # Randomise ordering
#     random.shuffle(start)
#     random.shuffle(target)

#     # Exact minimum number of cuts
#     truth = n - m

#     # Return problem and known truth
#     return start,target,truth

# # Test accuracy of solve4 as a function of n for different m
# def test_accuracy(max_n=30,n_tests=1000):

#     # Create figure
#     plt.figure()

#     # Loop over number of starting bars
#     for m in range(1,11):

#         # Store n values
#         n_values = []

#         # Store accuracy at each n
#         accuracies = []

#         # n must be >= m
#         for n in range(m,max_n+1):

#             # Number correctly solved
#             correct = 0

#             # Generate n_tests random problems
#             for i in range(n_tests):

#                 # Generate random test with known exact solution
#                 start,target,truth = generate_truth_test(m,n)

#                 # Solve using solve4
#                 result = solve4(start.copy(),target.copy())

#                 # Check against known optimum
#                 if result == truth:
#                     correct += 1

#             # Calculate percentage accuracy
#             accuracy = 100*correct/n_tests

#             # Store results
#             n_values.append(n)
#             accuracies.append(accuracy)

#             # Print progress/results
#             print(f"m = {m}, n = {n}, accuracy = {accuracy:.2f}%")

#         # Plot this value of m
#         plt.plot(n_values,accuracies,label=f"m = {m}")

#     # Label axes
#     plt.xlabel("Number of children, n")
#     plt.ylabel("Accuracy (%)")

#     # Set accuracy range
#     plt.ylim(0,105)

#     # Add legend
#     plt.legend()

#     # Add grid
#     plt.grid()

#     # Display plot
#     plt.show()

# Test accuracy of solve4 as a function of n for different m
def test_accuracy(max_n=30,n_tests=1000):

    # Dictionary to store all results
    results = {}

    # Loop over number of starting bars
    for m in range(1,11):

        # Store results for this value of m
        results[m] = []

        # n must be >= m
        for n in range(m,max_n+1):

            # Number correctly solved
            correct = 0

            # Generate n_tests random problems
            for i in range(n_tests):

                # Generate random test with known exact solution
                start,target,truth = generate_truth_test(m,n)

                # Solve using solve4
                result = solve4(start.copy(),target.copy())

                # Check that result is not below known minimum
                if result < truth:
                    raise RuntimeError(
                        f"solve4 returned fewer than the true minimum: "
                        f"start={start}, target={target}, truth={truth}, result={result}"
                    )

                # Check against known optimum
                if result == truth:
                    correct += 1

            # Calculate percentage accuracy
            accuracy = 100*correct/n_tests

            # Store results
            results[m].append((n,accuracy))

            # Print progress/results
            print(f"m = {m}, n = {n}, accuracy = {accuracy:.2f}%")

    # -------------------------------------------------------------------------
    # Plot accuracy as a function of n
    # -------------------------------------------------------------------------

    # Create figure
    plt.figure()

    # Loop over number of starting bars
    for m in range(1,11):

        # Get n values
        n_values = [result[0] for result in results[m]]

        # Get accuracies
        accuracies = [result[1] for result in results[m]]

        # Plot this value of m
        plt.plot(n_values,accuracies,label=f"m = {m}")

    # Label axes
    plt.xlabel("Number of children, n")
    plt.ylabel("Accuracy (%)")

    # Set accuracy range
    plt.ylim(0,105)

    # Add legend
    plt.legend()

    # Add grid
    plt.grid()

    # -------------------------------------------------------------------------
    # Plot accuracy as a function of n/m
    # -------------------------------------------------------------------------

    # Create figure
    plt.figure()

    # Loop over number of starting bars
    for m in range(1,11):

        # Get n/m values
        nm_values = [result[0]/m for result in results[m]]

        # Get accuracies
        accuracies = [result[1] for result in results[m]]

        # Plot this value of m
        plt.plot(nm_values,accuracies,label=f"m = {m}")

    # Label axes
    plt.xlabel("Number of children per starting bar, n/m")
    plt.ylabel("Accuracy (%)")

    # Set accuracy range
    plt.ylim(0,105)

    # Add legend
    plt.legend()

    # Add grid
    plt.grid()

    # Display both plots
    plt.show()

# Test accuracy of solve4 as a function of m for fixed n/m
def test_accuracy_fixed_ratio(max_m=30,n_tests=1000):

    # Ratios of number of children to number of starting bars
    ratios = [1,1.5,2,2.5,3,4,5]

    # Create figure
    plt.figure()

    # Loop over n/m ratios
    for ratio in ratios:

        # Store m values
        m_values = []

        # Store accuracies
        accuracies = []

        # Loop over number of starting bars
        for m in range(1,max_m+1):

            # Calculate corresponding number of children
            n = ratio*m

            # Skip if n is not an integer
            if not n.is_integer():
                continue

            # Convert n to integer
            n = int(n)

            # Number correctly solved
            correct = 0

            # Generate n_tests random problems
            for i in range(n_tests):

                # Generate random test with known exact solution
                start,target,truth = generate_truth_test(m,n)

                # Solve using solve4
                result = solve4(start.copy(),target.copy())

                # Check that result is not below known minimum
                if result < truth:
                    raise RuntimeError(
                        f"solve4 returned fewer than the true minimum: "
                        f"start={start}, target={target}, truth={truth}, result={result}"
                    )

                # Check against known optimum
                if result == truth:
                    correct += 1

            # Calculate percentage accuracy
            accuracy = 100*correct/n_tests

            # Store results
            m_values.append(m)
            accuracies.append(accuracy)

            # Print progress/results
            print(
                f"n/m = {ratio}, m = {m}, n = {n}, "
                f"accuracy = {accuracy:.2f}%"
            )

        # Plot this value of n/m
        plt.plot(m_values,accuracies,label=f"n/m = {ratio}")

    # Label axes
    plt.xlabel("Number of starting bars, m")
    plt.ylabel("Accuracy (%)")

    # Set accuracy range
    plt.ylim(0,105)

    # Add legend
    plt.legend()

    # Add grid
    plt.grid()

    # Display plot
    plt.show()
    
# # Number of random tests
# n_tests = 10000

# # Number correctly solved
# correct = 0

# # Loop through random tests
# for i in range(n_tests):

#     # Random number of starting bars
#     m = random.randint(1,10)

#     # Random number of targets, ensuring n >= m
#     n = random.randint(m,20)

#     # Generate random test with known exact solution
#     start,target,truth = generate_truth_test(m,n)

#     # Solve using solve4
#     result = solve4(start.copy(),target.copy())

#     # Check against known optimum
#     if result == truth:
#         correct += 1

# # Print accuracy
# print(f"Correct = {correct}/{n_tests} ({100*correct/n_tests:.2f}%)")

# test_accuracy(max_n=30,n_tests=1000)
# test_accuracy_fixed_ratio(max_m=30,n_tests=1000)
