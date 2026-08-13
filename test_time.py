import random
import time
import numpy as np
import matplotlib.pyplot as plt

from generate_truths import generate_truth_test
from solve4 import solve4

# Generate all (m,n) cases for tests as a function of n
def generate_size_cases(max_n=30,max_m=10):

    # Store all cases
    cases = []

    # Loop over number of starting bars
    for m in range(1,max_m+1):

        # n must be >= m
        for n in range(m,max_n+1):
            cases.append((m,n))

    # Return all cases
    return cases

# Generate all (m,n) cases for tests with fixed n/m
def generate_ratio_cases(max_m=30,ratios=None):

    # Ratios of number of children to number of starting bars
    if ratios is None:
        ratios = [1,1.5,2,2.5,3,4,5]

    # Store all cases and their ratios
    cases = []

    # Loop over n/m ratios
    for ratio in ratios:

        # Loop over number of starting bars
        for m in range(1,max_m+1):

            # Calculate corresponding number of children
            n = ratio*m

            # Skip if n is not an integer
            if not float(n).is_integer():
                continue

            # Store case
            cases.append((m,int(n),ratio))

    # Return all cases
    return cases

# Generate and solve one set of trials for a given (m,n) case
def run_trials(m,n,n_tests):

    # Store all trial results
    trials = []

    # Generate n_tests random problems
    for i in range(n_tests):

        # Generate random test with known exact solution
        start,target,truth = generate_truth_test(m,n)

        # Copy inputs because solve4 modifies them
        test_start = start.copy()
        test_target = target.copy()

        # Get start time
        t0 = time.perf_counter()

        # Solve using solve4
        solver_output = solve4(test_start,test_target)

        # Get end time
        t1 = time.perf_counter()

        # Get number of cuts from solve4 result
        if isinstance(solver_output,dict):
            result = solver_output["cuts"]
        else:
            result = solver_output

        # Check that result is not below known minimum
        if result < truth:
            raise RuntimeError(
                f"solve4 returned fewer than the true minimum: "
                f"start={start}, target={target}, truth={truth}, result={result}"
            )

        # Store problem, result and computation time
        trials.append({
            "start": start,
            "target": target,
            "truth": truth,
            "result": result,
            "solver_output": solver_output,
            "time": t1-t0
        })

    # Return all trials
    return trials

# Run each (m,n) case once and store shared trial results
def run_experiment(cases,n_tests=1000,seed=None):

    # Set random seed if supplied
    if seed is not None:
        random.seed(seed)

    # Dictionary to store all results
    results = {}

    # Run all cases
    for case in cases:
        m,n = case[:2]
        results[(m,n)] = run_trials(m,n,n_tests)

    # Return shared results for accuracy and timing analysis
    return results

# Calculate accuracy and timing summaries from recorded trials
def summarise_results(results):

    # Dictionary to store all summaries
    summaries = {}

    # Loop over all (m,n) cases
    for case,trials in results.items():

        # Number correctly solved
        correct = sum(
            trial["result"] == trial["truth"]
            for trial in trials
        )

        # Get recorded computation times
        times = [trial["time"] for trial in trials]

        # Store accuracy and timing summaries
        summaries[case] = {
            "accuracy": 100*correct/len(trials),
            "median_time": np.median(times)*1e6,
            "mean_time": np.mean(times)*1e6
        }

    # Return summaries
    return summaries

# Get cases for one value of m
def get_m_cases(summaries,m):
    return sorted(case for case in summaries if case[0] == m)

# Get cases for one value of n/m
def get_ratio_cases(summaries,ratio):
    return sorted(
        case for case in summaries
        if case[1]/case[0] == ratio
    )

# Plot accuracy as a function of n and n/m
def plot_size_accuracy(summaries):

    # Get all values of m
    m_values = sorted(set(m for m,n in summaries))

    # Create accuracy plot as a function of n
    plt.figure()

    for m in m_values:
        cases = get_m_cases(summaries,m)
        n_values = [n for _,n in cases]
        accuracies = [summaries[case]["accuracy"] for case in cases]
        plt.plot(n_values,accuracies,label=f"m = {m}")

    # Label and format axes
    plt.xlabel("Number of children, n")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0,105)
    plt.legend()
    plt.grid()

    # Create accuracy plot as a function of n/m
    plt.figure()

    for m in m_values:
        cases = get_m_cases(summaries,m)
        nm_values = [n/m for _,n in cases]
        accuracies = [summaries[case]["accuracy"] for case in cases]
        plt.plot(nm_values,accuracies,label=f"m = {m}")

    # Label and format axes
    plt.xlabel("Number of children per starting bar, n/m")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0,105)
    plt.legend()
    plt.grid()

# Plot computation time as a function of n and n/m
def plot_size_time(summaries):

    # Get all values of m
    m_values = sorted(set(m for m,n in summaries))

    # Create timing plot as a function of n
    plt.figure()

    for m in m_values:
        cases = get_m_cases(summaries,m)
        n_values = [n for _,n in cases]
        times = [summaries[case]["median_time"] for case in cases]
        plt.plot(n_values,times,label=f"m = {m}")

    # Label and format axes
    plt.xlabel("Number of children, n")
    plt.ylabel("Median computation time (us)")
    plt.legend()
    plt.grid()

    # Create timing plot as a function of n/m
    plt.figure()

    for m in m_values:
        cases = get_m_cases(summaries,m)
        nm_values = [n/m for _,n in cases]
        times = [summaries[case]["median_time"] for case in cases]
        plt.plot(nm_values,times,label=f"m = {m}")

    # Label and format axes
    plt.xlabel("Number of children per starting bar, n/m")
    plt.ylabel("Median computation time (us)")
    plt.legend()
    plt.grid()

# Plot accuracy as a function of m for fixed n/m
def plot_ratio_accuracy(summaries,ratios):

    # Create figure
    plt.figure()

    # Loop over n/m ratios
    for ratio in ratios:
        cases = get_ratio_cases(summaries,ratio)
        m_values = [m for m,n in cases]
        accuracies = [summaries[case]["accuracy"] for case in cases]
        plt.plot(m_values,accuracies,label=f"n/m = {ratio}")

    # Label and format axes
    plt.xlabel("Number of starting bars, m")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0,105)
    plt.legend()
    plt.grid()

# Plot computation time as a function of m for fixed n/m
def plot_ratio_time(summaries,ratios,fit_start=10):

    # Create figure
    plt.figure()

    # Store calculated scaling exponents
    exponents = {}

    # Loop over n/m ratios
    for ratio in ratios:
        cases = get_ratio_cases(summaries,ratio)
        m_values = np.array([m for m,n in cases])
        median_times = np.array([
            summaries[case]["median_time"] for case in cases
        ])

        # Plot this value of n/m
        plt.loglog(m_values,median_times,label=f"n/m = {ratio}")

        # Only fit larger problems
        mask = m_values >= fit_start

        # Need at least two points to fit a line
        if np.count_nonzero(mask) >= 2:
            slope,intercept = np.polyfit(
                np.log(m_values[mask]),
                np.log(median_times[mask]),
                1
            )

            exponents[ratio] = slope
            print(
                f"n/m = {ratio}, "
                f"large-m scaling exponent = {slope:.2f}"
            )

    # Label and format axes
    plt.xlabel("Number of starting bars, m")
    plt.ylabel("Median computation time (us)")
    plt.legend()
    plt.grid()

    # Return calculated scaling exponents
    return exponents

# Test accuracy and computation time as a function of n for different m
def test_by_size(max_n=30,n_tests=1000,seed=None):

    # Generate and solve each trial once
    cases = generate_size_cases(max_n)
    results = run_experiment(cases,n_tests,seed)

    # Calculate accuracy and timing from the same trials
    summaries = summarise_results(results)

    # Print progress/results
    for m,n in sorted(summaries):
        summary = summaries[(m,n)]
        print(
            f"m = {m}, n = {n}, "
            f"accuracy = {summary['accuracy']:.2f}%, "
            f"median time = {summary['median_time']:.2f} us"
        )

    # Plot shared results
    plot_size_accuracy(summaries)
    plot_size_time(summaries)
    plt.show()

    # Return raw results so they can be analysed without rerunning trials
    return results

# Test accuracy and computation time as a function of m for fixed n/m
def test_fixed_ratio(max_m=30,n_tests=1000,seed=None):

    # Ratios of number of children to number of starting bars
    ratios = [1,1.5,2,2.5,3,4,5]

    # Generate and solve each trial once
    ratio_cases = generate_ratio_cases(max_m,ratios)
    cases = [(m,n) for m,n,ratio in ratio_cases]
    results = run_experiment(cases,n_tests,seed)

    # Calculate accuracy and timing from the same trials
    summaries = summarise_results(results)

    # Print progress/results
    for m,n,ratio in ratio_cases:
        summary = summaries[(m,n)]
        print(
            f"n/m = {ratio}, m = {m}, n = {n}, "
            f"accuracy = {summary['accuracy']:.2f}%, "
            f"median time = {summary['median_time']:.2f} us"
        )

    # Plot shared results
    plot_ratio_accuracy(summaries,ratios)
    plot_ratio_time(summaries,ratios)
    plt.show()

    # Return raw results so they can be analysed without rerunning trials
    return results
