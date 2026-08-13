import time
import random
import numpy as np
import matplotlib.pyplot as plt

from generate_truths import gen_states
from solve4 import solve4

# Generate all (m,n) cases for tests as a function of n
def generate_cases(max_n=30,max_m=10):
    # Store all cases
    cases = []
    # Loop over number of starting bars
    for m in range(1,max_m+1):
        # n must be >= m
        for n in range(m,max_n+1):
            cases.append((m,n))
    # Return all cases
    return cases

# Generate and solve one set of trials for a given (m,n) case
def run_trials(func,m,n,n_tests):

    # Store all trial results
    trials = []

    # Generate n_tests random problems
    for i in range(n_tests):

        # Generate random test with known exact solution
        start,target,truth = gen_states(m,n)

        # Copy inputs because solve4 modifies them
        test_start = start.copy()
        test_target = target.copy()

        # Get start time
        t0 = time.perf_counter()

        # Solve using solve4
        #solver_output = solve4(test_start,test_target)
        solver_output = func[1](test_start,test_target)

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
def run_experiment(func,cases,n_tests=1000,seed=None):

    # Set random seed if supplied
    if seed is not None:
        random.seed(seed)

    # Dictionary to store all results
    results = {}

    # Run all cases
    for case in cases:
        m,n = case[:2]
        results[(m,n)] = run_trials(func,m,n,n_tests)

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

# Build a distinct filename for each plot
def get_plot_filename(func_name,summaries,n_tests,plot_type,plot_variant):
    max_m = max(m for m,n in summaries)
    max_n = max(n for m,n in summaries)
    safe_func_name = "".join(
        character if character.isalnum() or character in "-_" else "_"
        for character in func_name
    )
    return (
        f"plots/{safe_func_name}_max_m_{max_m}_max_n_{max_n}_"
        f"n_tests_{n_tests}_{plot_type}_{plot_variant}.png"
    )

# Plot accuracy as a function of n and n/m
def plot_accuracy(func_name,summaries,n_tests):
    
    # Get all values of m
    m_values = sorted(set(m for m,n in summaries))

    # Create accuracy plot as a function of n
    figure = plt.figure()

    # Plot title
    plt.title(f"{func_name}: accuracy as a function of n")
    
    for m in m_values:
        cases = get_m_cases(summaries,m)
        n_values = [n for _,n in cases]
        accuracies = [summaries[case]["accuracy"] for case in cases]
        plt.plot(n_values,accuracies,marker="o",label=f"m = {m}")

    # Label and format axes
    plt.xlabel("Number of children, n")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0,105)
    plt.legend()
    plt.grid()
    figure.savefig(
        get_plot_filename(func_name,summaries,n_tests,"accuracy","vs_n"),
        bbox_inches="tight"
    )

    # Create accuracy plot as a function of n/m
    figure = plt.figure()

    # Plot title
    plt.title(f"{func_name}: accuracy as a function of n/m")
    
    for m in m_values:
        cases = get_m_cases(summaries,m)
        nm_values = [n/m for _,n in cases]
        accuracies = [summaries[case]["accuracy"] for case in cases]
        plt.plot(nm_values,accuracies,marker="o",label=f"m = {m}")

    # Label and format axes
    plt.xlabel("Number of children per starting bar, n/m")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0,105)
    plt.legend()
    plt.grid()
    figure.savefig(
        get_plot_filename(func_name,summaries,n_tests,"accuracy","vs_n_per_m"),
        bbox_inches="tight"
    )

# Plot computation time as a function of n and n/m
def plot_time(func_name,summaries,n_tests):
    
    # Get all values of m
    m_values = sorted(set(m for m,n in summaries))

    # Create timing plot as a function of n
    figure = plt.figure()

    # Plot title
    plt.title(f"{func_name}: median time as a function of n")
    
    for m in m_values:
        cases = get_m_cases(summaries,m)
        n_values = [n for _,n in cases]
        times = [summaries[case]["median_time"] for case in cases]
        plt.plot(n_values,times,marker="o",label=f"m = {m}")

    # Label and format axes
    plt.xlabel("Number of children, n")
    plt.ylabel("Median computation time (us)")
    plt.legend()
    plt.grid()
    figure.savefig(
        get_plot_filename(func_name,summaries,n_tests,"time","median_vs_n"),
        bbox_inches="tight"
    )

    # Create timing plot as a function of n/m
    figure = plt.figure()

    # Plot title
    plt.title(f"{func_name}: median time as a function of n/m")
    
    for m in m_values:
        cases = get_m_cases(summaries,m)
        nm_values = [n/m for _,n in cases]
        times = [summaries[case]["median_time"] for case in cases]
        plt.plot(nm_values,times,marker="o",label=f"m = {m}")

    # Label and format axes
    plt.xlabel("Number of children per starting bar, n/m")
    plt.ylabel("Median computation time (us)")
    plt.legend()
    plt.grid()
    figure.savefig(
        get_plot_filename(func_name,summaries,n_tests,"time","median_vs_n_per_m"),
        bbox_inches="tight"
    )

# Plot results for multiple functions together
def plot_comparison(summaries_by_func,n_tests,plot_type,plot_variant):

    # Use colour for m and line style for function
    figure = plt.figure()
    line_styles = ["-","--","-.",":"]
    func_names = list(summaries_by_func)
    all_summaries = next(iter(summaries_by_func.values()))
    m_values = sorted(set(m for m,n in all_summaries))
    colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    for func_index,(func_name,summaries) in enumerate(summaries_by_func.items()):
        for m_index,m in enumerate(m_values):
            cases = get_m_cases(summaries,m)

            if plot_variant == "vs_n":
                x_values = [n for _,n in cases]
            else:
                x_values = [n/m for _,n in cases]

            if plot_type == "accuracy":
                y_values = [summaries[case]["accuracy"] for case in cases]
            else:
                y_values = [summaries[case]["median_time"] for case in cases]

            plt.plot(
                x_values,y_values,
                color=colours[m_index % len(colours)],
                linestyle=line_styles[func_index % len(line_styles)],
                marker="o",
                label=f"{func_name}, m = {m}"
            )

    if plot_variant == "vs_n":
        plt.xlabel("Number of children, n")
    else:
        plt.xlabel("Number of children per starting bar, n/m")

    if plot_type == "accuracy":
        plt.title("Accuracy comparison")
        plt.ylabel("Accuracy (%)")
        plt.ylim(0,105)
    else:
        plt.title("Median computation time comparison")
        plt.ylabel("Median computation time (us)")

    plt.legend()
    plt.grid()
    figure.savefig(
        get_plot_filename(
            "_vs_".join(func_names),all_summaries,n_tests,
            f"combined_{plot_type}",plot_variant
        ),
        bbox_inches="tight"
    )

# Test accuracy and computation time as a function of n for different m
def run_analysis(func,max_n=30,n_tests=1000,seed=None,max_m=10):

    # Generate all (m,n) cases for tests as a function of n
    cases = generate_cases(max_n,max_m)

    # Accept either one function tuple or a list of function tuples
    if isinstance(func,tuple):
        funcs = [func]
    else:
        funcs = func

    # Store results and summaries for each function
    results_by_func = {}
    summaries_by_func = {}

    for current_func in funcs:
        results = run_experiment(current_func,cases,n_tests,seed)
        summaries = summarise_results(results)
        results_by_func[current_func[0]] = results
        summaries_by_func[current_func[0]] = summaries

        # Plot each function separately
        plot_accuracy(current_func[0],summaries,n_tests)
        plot_time(current_func[0],summaries,n_tests)

    # Plot all functions together when there is more than one
    if len(funcs) > 1:
        plot_comparison(summaries_by_func,n_tests,"accuracy","vs_n")
        plot_comparison(summaries_by_func,n_tests,"accuracy","vs_n_per_m")
        plot_comparison(summaries_by_func,n_tests,"time","vs_n")
        plot_comparison(summaries_by_func,n_tests,"time","vs_n_per_m")

    plt.show()

    # Return raw results so they can be analysed without rerunning trials
    if len(funcs) == 1:
        return results_by_func[funcs[0][0]]
    return results_by_func
