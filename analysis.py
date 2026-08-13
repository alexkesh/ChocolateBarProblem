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

            # Store this valid (m,n) pair
            cases.append((m,n))

    # Return all cases
    return cases

# Generate and solve one set of trials for a given (m,n) case
def run_trials(func,m,n,n_tests):

    # Store all trial results
    trials = []

    # Generate n_tests random problems
    for _ in range(n_tests):

        # Generate random test with known exact solution
        start,target,truth = gen_states(m,n)

        # Copy inputs in case the solver modifies them
        test_start = start.copy()
        test_target = target.copy()

        # Get start time
        t0 = time.perf_counter()

        # Get the solver function from the (name,function) tuple and run it
        solver_output = func[1](test_start,test_target)

        # Get end time
        t1 = time.perf_counter()

        # Get number of cuts from a dictionary result
        if isinstance(solver_output,dict):
            result = solver_output["cuts"]
        # Otherwise use the value returned directly by an earlier solver
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

        # Get m and n from this case
        m,n = case[:2]

        # Run every trial for this case and store the results under (m,n)
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

        # Number of trials in this case
        n_trials = len(trials)

        # Get recorded computation times
        times = [trial["time"] for trial in trials]

        # Store accuracy and timing summaries
        summaries[case] = {
            "accuracy": 100*correct/n_trials,
            "median_time": np.median(times)*1e6,
            "mean_time": np.mean(times)*1e6
        }

    # Return summaries
    return summaries

# Get cases for one value of m
def get_m_cases(summaries,m):

    # Return matching cases in increasing (m,n) order
    return sorted(case for case in summaries if case[0] == m)

# Build a distinct filename for each plot
def get_plot_filename(func_name,summaries,n_tests,plot_type,plot_variant):

    # Get the largest m represented in this analysis
    max_m = max(m for m,n in summaries)

    # Get the largest n represented in this analysis
    max_n = max(n for m,n in summaries)

    # Replace characters which may not be safe in a filename
    safe_func_name = "".join(
        character if character.isalnum() or character in "-_" else "_"
        for character in func_name
    )

    # Include all analysis settings and the plot variant in the filename
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

    # Plot one line for each value of m
    for m in m_values:

        # Get all cases for this value of m
        cases = get_m_cases(summaries,m)

        # Get the n value for each case
        n_values = [n for _,n in cases]

        # Get the recorded accuracy for each case
        accuracies = [summaries[case]["accuracy"] for case in cases]

        # Plot accuracy against n
        plt.plot(n_values,accuracies,marker="o",label=f"m = {m}")

    # Label and format axes
    plt.xlabel("Number of children, n")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0,105)
    plt.legend()
    plt.grid()

    # Save the completed plot
    figure.savefig(
        get_plot_filename(func_name,summaries,n_tests,"accuracy","vs_n"),
        bbox_inches="tight"
    )

    # Close the figure so a large analysis does not keep it in memory
    plt.close(figure)

    # Create accuracy plot as a function of n/m
    figure = plt.figure()

    # Plot title
    plt.title(f"{func_name}: accuracy as a function of n/m")

    # Plot one line for each value of m
    for m in m_values:

        # Get all cases for this value of m
        cases = get_m_cases(summaries,m)

        # Calculate n/m for each case
        nm_values = [n/m for _,n in cases]

        # Get the recorded accuracy for each case
        accuracies = [summaries[case]["accuracy"] for case in cases]

        # Plot accuracy against n/m
        plt.plot(nm_values,accuracies,marker="o",label=f"m = {m}")

    # Label and format axes
    plt.xlabel("Number of children per starting bar, n/m")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0,105)
    plt.legend()
    plt.grid()

    # Save the completed plot
    figure.savefig(
        get_plot_filename(func_name,summaries,n_tests,"accuracy","vs_n_per_m"),
        bbox_inches="tight"
    )

    # Close the figure so a large analysis does not keep it in memory
    plt.close(figure)

# Plot computation time as a function of n and n/m
def plot_time(func_name,summaries,n_tests):
    
    # Get all values of m
    m_values = sorted(set(m for m,n in summaries))

    # Create timing plot as a function of n
    figure = plt.figure()

    # Plot title
    plt.title(f"{func_name}: median time as a function of n")

    # Plot one line for each value of m
    for m in m_values:

        # Get all cases for this value of m
        cases = get_m_cases(summaries,m)

        # Get the n value for each case
        n_values = [n for _,n in cases]

        # Get the recorded median time for each case
        times = [summaries[case]["median_time"] for case in cases]

        # Plot median time against n
        plt.plot(n_values,times,marker="o",label=f"m = {m}")

    # Label and format axes
    plt.xlabel("Number of children, n")
    plt.ylabel("Median computation time (us)")
    plt.legend()
    plt.grid()

    # Save the completed plot
    figure.savefig(
        get_plot_filename(func_name,summaries,n_tests,"time","median_vs_n"),
        bbox_inches="tight"
    )

    # Close the figure so a large analysis does not keep it in memory
    plt.close(figure)

    # Create timing plot as a function of n/m
    figure = plt.figure()

    # Plot title
    plt.title(f"{func_name}: median time as a function of n/m")

    # Plot one line for each value of m
    for m in m_values:

        # Get all cases for this value of m
        cases = get_m_cases(summaries,m)

        # Calculate n/m for each case
        nm_values = [n/m for _,n in cases]

        # Get the recorded median time for each case
        times = [summaries[case]["median_time"] for case in cases]

        # Plot median time against n/m
        plt.plot(nm_values,times,marker="o",label=f"m = {m}")

    # Label and format axes
    plt.xlabel("Number of children per starting bar, n/m")
    plt.ylabel("Median computation time (us)")
    plt.legend()
    plt.grid()

    # Save the completed plot
    figure.savefig(
        get_plot_filename(func_name,summaries,n_tests,"time","median_vs_n_per_m"),
        bbox_inches="tight"
    )

    # Close the figure so a large analysis does not keep it in memory
    plt.close(figure)

# Get the difference between cuts found and the known minimum for every trial
def get_cut_differences(results):

    # Flatten all cases into one list of additional-cut values
    return [
        trial["result"]-trial["truth"]
        for trials in results.values()
        for trial in trials
    ]

# Plot a histogram of the additional cuts used above the known minimum
def plot_cut_differences(results_by_func,summaries_by_func,n_tests):

    # Get every cut difference for each solver function
    differences_by_func = {
        func_name: get_cut_differences(results)
        for func_name,results in results_by_func.items()
    }

    # Keep only trials where the solver used one or more additional cuts
    non_optimal_by_func = {
        func_name: [difference for difference in differences if difference >= 1]
        for func_name,differences in differences_by_func.items()
    }

    # Store all non-optimal differences in one list
    all_non_optimal = [
        difference
        for non_optimal in non_optimal_by_func.values()
        for difference in non_optimal
    ]

    # Get the largest cut difference, using 1 if every trial was optimal
    max_difference = max(
        all_non_optimal,
        default=1
    )

    # Use common integer-centred bins so functions can be compared directly
    bins = np.arange(0.5,max_difference+1.5,1)

    # Get one summary dictionary to read the shared analysis limits
    first_summaries = next(iter(summaries_by_func.values()))

    # Get the largest m represented in the analysis
    max_m = max(m for m,n in first_summaries)

    # Get the largest n represented in the analysis
    max_n = max(n for m,n in first_summaries)

    # Plot each function separately
    for func_name,differences in differences_by_func.items():

        # Get only the non-optimal trials for this function
        non_optimal = non_optimal_by_func[func_name]

        # Count all trials and non-optimal trials for this function
        total_trials = len(differences)
        n_non_optimal = len(non_optimal)

        # Calculate the percentage of all trials which were non-optimal
        non_optimal_percentage = 100*n_non_optimal/total_trials

        # Produce both linear and logarithmic y-axis versions
        for y_scale in ["linear","log"]:

            # Create a new histogram figure
            figure = plt.figure()

            # Plot the non-optimal trials if any exist
            if non_optimal:

                # Weight each trial as a percentage of all trials
                weights = np.ones(n_non_optimal)*100/total_trials

                # Plot one bar for each integer cut difference
                plt.hist(
                    non_optimal,
                    bins=bins,
                    weights=weights,
                    edgecolor="black"
                )

            # Otherwise state that every trial found the minimum
            else:
                plt.text(
                    0.5,0.5,"No non-optimal trials",
                    transform=plt.gca().transAxes,
                    horizontalalignment="center",
                    verticalalignment="center"
                )

            # Label and format axes
            plt.title(f"{func_name}: error size for non-optimal trials")
            plt.xlabel("Additional cuts above minimum")
            plt.ylabel("Trials (% of total)")
            plt.xticks(range(1,max_difference+1))
            plt.yscale(y_scale)

            # Give an empty logarithmic plot a valid positive y-axis range
            if y_scale == "log" and not non_optimal:
                plt.ylim(0.1,100)

            # Add horizontal grid lines
            plt.grid(axis="y")

            # Display the analysis settings and non-optimal trial count
            plt.text(
                0.98,0.95,
                f"max m = {max_m}\nmax n = {max_n}\n"
                f"trials per (m,n) = {n_tests:,}\n"
                f"non-optimal trials = {n_non_optimal:,} "
                f"({non_optimal_percentage:.2f}%)\n"
                f"total trials = {total_trials:,}",
                transform=plt.gca().transAxes,
                horizontalalignment="right",
                verticalalignment="top",
                bbox={"facecolor": "white","alpha": 0.8,"edgecolor": "grey"}
            )

            # Save a distinct file for this solver and y-axis scale
            figure.savefig(
                get_plot_filename(
                    func_name,summaries_by_func[func_name],n_tests,
                    "accuracy",f"cut_difference_histogram_{y_scale}"
                ),
                bbox_inches="tight"
            )

            # Close the figure so a large analysis does not keep it in memory
            plt.close(figure)

    # Plot functions together when there is more than one
    if len(differences_by_func) > 1:

        # Keep function names in their original order for labels and filename
        func_names = list(differences_by_func)

        # Every function has the same number of trials in a comparison
        total_trials = len(next(iter(differences_by_func.values())))

        # Build one annotation line for each function
        error_summary = "\n".join(
            f"{func_name} non-optimal = {len(non_optimal):,} "
            f"({100*len(non_optimal)/len(differences_by_func[func_name]):.2f}%)"
            for func_name,non_optimal in non_optimal_by_func.items()
        )

        # Produce both linear and logarithmic y-axis versions
        for y_scale in ["linear","log"]:

            # Create a new comparison histogram figure
            figure = plt.figure()

            # Plot one outline histogram for each function
            for func_name,differences in differences_by_func.items():

                # Get non-optimal trials for this function
                non_optimal = non_optimal_by_func[func_name]

                # Plot the non-optimal trials if any exist
                if non_optimal:

                    # Weight each trial as a percentage of all function trials
                    weights = np.ones(len(non_optimal))*100/len(differences)

                    # Use an outline so functions do not cover one another
                    plt.hist(
                        non_optimal,
                        bins=bins,
                        weights=weights,
                        histtype="step",
                        linewidth=2,
                        label=func_name
                    )

                # Keep a legend entry when every trial was optimal
                else:
                    plt.plot([],[],label=f"{func_name} (no non-optimal trials)")

            # State clearly if every function found the minimum every time
            if not any(non_optimal_by_func.values()):
                plt.text(
                    0.5,0.5,"No non-optimal trials",
                    transform=plt.gca().transAxes,
                    horizontalalignment="center",
                    verticalalignment="center"
                )

            # Label and format axes
            plt.title("Error size comparison for non-optimal trials")
            plt.xlabel("Additional cuts above minimum")
            plt.ylabel("Trials (% of total)")
            plt.xticks(range(1,max_difference+1))
            plt.yscale(y_scale)

            # Give an empty logarithmic plot a valid positive y-axis range
            if y_scale == "log" and not any(non_optimal_by_func.values()):
                plt.ylim(0.1,100)

            # Add function labels and horizontal grid lines
            plt.legend(loc="upper left")
            plt.grid(axis="y")

            # Display the analysis settings and non-optimal count per function
            plt.text(
                0.98,0.95,
                f"max m = {max_m}\nmax n = {max_n}\n"
                f"trials per (m,n) = {n_tests:,}\n"
                f"{error_summary}\n"
                f"total trials per function = {total_trials:,}",
                transform=plt.gca().transAxes,
                horizontalalignment="right",
                verticalalignment="top",
                bbox={"facecolor": "white","alpha": 0.8,"edgecolor": "grey"}
            )

            # Save a distinct file for this comparison and y-axis scale
            figure.savefig(
                get_plot_filename(
                    "_vs_".join(func_names),first_summaries,n_tests,
                    "combined_accuracy",f"cut_difference_histogram_{y_scale}"
                ),
                bbox_inches="tight"
            )

            # Close the figure so a large analysis does not keep it in memory
            plt.close(figure)

# Plot results for multiple functions together
def plot_comparison(summaries_by_func,n_tests,plot_type,plot_variant):

    # Create a new comparison figure
    figure = plt.figure()

    # Use a different line style for each function
    line_styles = ["-","--","-.",":"]

    # Keep function names in their original order for labels and filename
    func_names = list(summaries_by_func)

    # Get one summary dictionary to read the shared values of m
    first_summaries = next(iter(summaries_by_func.values()))

    # Get every value of m represented in the comparison
    m_values = sorted(set(m for m,n in first_summaries))

    # Use a different colour for each value of m
    colours = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    # Loop over every function and its summary results
    for func_index,(func_name,summaries) in enumerate(summaries_by_func.items()):

        # Loop over every value of m for this function
        for m_index,m in enumerate(m_values):

            # Get all cases for this value of m
            cases = get_m_cases(summaries,m)

            # Use n values for a plot against n
            if plot_variant == "vs_n":
                x_values = [n for _,n in cases]

            # Otherwise calculate n/m for a plot against n/m
            else:
                x_values = [n/m for _,n in cases]

            # Use accuracy values for an accuracy comparison
            if plot_type == "accuracy":
                y_values = [summaries[case]["accuracy"] for case in cases]

            # Otherwise use median times for a timing comparison
            else:
                y_values = [summaries[case]["median_time"] for case in cases]

            # Use colour for m and line style for function
            plt.plot(
                x_values,y_values,
                color=colours[m_index % len(colours)],
                linestyle=line_styles[func_index % len(line_styles)],
                marker="o",
                label=f"{func_name}, m = {m}"
            )

    # Label the x-axis for a plot against n
    if plot_variant == "vs_n":
        plt.xlabel("Number of children, n")

    # Label the x-axis for a plot against n/m
    else:
        plt.xlabel("Number of children per starting bar, n/m")

    # Label and format an accuracy comparison
    if plot_type == "accuracy":
        plt.title("Accuracy comparison")
        plt.ylabel("Accuracy (%)")
        plt.ylim(0,105)

    # Label a median computation-time comparison
    else:
        plt.title("Median computation time comparison")
        plt.ylabel("Median computation time (us)")

    # Add function labels and grid lines
    plt.legend()
    plt.grid()

    # Save a distinct file for this plot type and x-axis variant
    figure.savefig(
        get_plot_filename(
            "_vs_".join(func_names),first_summaries,n_tests,
            f"combined_{plot_type}",plot_variant
        ),
        bbox_inches="tight"
    )

    # Close the figure so a large analysis does not keep it in memory
    plt.close(figure)

# Test accuracy and computation time as a function of n for different m
def run_analysis(func,max_n=30,n_tests=1000,seed=None,max_m=10):

    # Generate all (m,n) cases for tests as a function of n
    cases = generate_cases(max_n,max_m)

    # Accept either one function tuple or a list of function tuples
    if isinstance(func,tuple):

        # Put one function tuple into a list for the shared loop below
        funcs = [func]

    # Otherwise use the supplied list of function tuples
    else:
        funcs = func

    # Store results and summaries for each function
    results_by_func = {}
    summaries_by_func = {}

    # Run and plot each function separately
    for current_func in funcs:

        # Get the function name from the (name,function) tuple
        func_name = current_func[0]

        # Run every generated case for this function
        results = run_experiment(current_func,cases,n_tests,seed)

        # Calculate accuracy and timing summaries from the raw trials
        summaries = summarise_results(results)

        # Store raw results under the function name
        results_by_func[func_name] = results

        # Store summary results under the function name
        summaries_by_func[func_name] = summaries

        # Plot each function separately
        plot_accuracy(func_name,summaries,n_tests)
        plot_time(func_name,summaries,n_tests)

    # Plot how far each trial was from the known minimum
    plot_cut_differences(results_by_func,summaries_by_func,n_tests)

    # Plot all functions together when there is more than one
    if len(funcs) > 1:

        # Compare accuracy against n
        plot_comparison(summaries_by_func,n_tests,"accuracy","vs_n")

        # Compare accuracy against n/m
        plot_comparison(summaries_by_func,n_tests,"accuracy","vs_n_per_m")

        # Compare median time against n
        plot_comparison(summaries_by_func,n_tests,"time","vs_n")

        # Compare median time against n/m
        plot_comparison(summaries_by_func,n_tests,"time","vs_n_per_m")

    # Return raw results so they can be analysed without rerunning trials
    if len(funcs) == 1:

        # Return the same result structure used before multi-function support
        return results_by_func[funcs[0][0]]

    # Return results under each function name for a comparison
    return results_by_func
