# Chocolate bar cutting problem - Alex Keshavarzi

This repository contains my solution to the chocolate bar cutting problem. Given `m` starting chocolate bars and the requested amounts for `n` children, the aim is to distribute the requested chocolate using as few cuts as possible.

The main solution is `solve4.py`. It uses a fast greedy approximation intended to remain practical as the inputs grow. `solve5.py` provides an exact reference solution for smaller cases, where an exhaustive search is still computationally feasible. The earlier solver files have been retained to show how the approach developed as I tested the problem and clarified its assumptions.

## Contents

1. [Problem interpretation](#1-problem-interpretation)
2. [Current approach](#2-current-approach)
3. [Repository structure](#3-repository-structure)
4. [File descriptions and connections](#4-file-descriptions-and-connections)
5. [Running the code](#5-running-the-code)
6. [Using the solvers directly](#6-using-the-solvers-directly)
7. [Trade-off](#7-trade-off)
8. [Analysis findings](#8-analysis-findings)

## 1. Problem interpretation

I explicitly checked the following assumptions and constraints with Jake:

- `start` is a list containing the sizes of the `m` starting chocolate bars.
- `target` is a list containing the amounts requested by the `n` children.
- All chocolate amounts are represented by positive integers.
- One cut splits one existing piece into exactly two new pieces.
- Both pieces created by a cut must have a size of at least one.
- Giving an existing whole piece to a child requires no cut.
- A child may receive several smaller pieces of chocolate.
- Those pieces may come from different starting bars.
- Not all available chocolate has to be used. A remainder is allowed, so `sum(target)` may be less than `sum(start)`.
- Ordering has no meaning. Neither input list is assumed to arrive sorted.
- Duplicate values are allowed in both lists. The children do not all request the same amount, but their individual requests do not have to be unique.
- A solution should not be assumed to exist. The program must handle cases where the children cannot all receive their requested amounts exactly.

For the final point, I chose to handle an infeasible total request as follows:

- If `sum(target) > sum(start)`, the targets are reduced proportionally to the available chocolate while ensuring that every child receives at least one unit.
- The returned `exact_target` flag is set to `False`, and `target_used` records the adjusted allocation, so the caller can see that the original requests were not met exactly.
- If there is not even one unit available per child, the fairness constraint cannot be met and `reduce_targets()` raises a `ValueError`.

The important clarification is that one child's allocation does not need to come from one contiguous piece or one starting bar. For example: {start = [3,3], target = [6]} requires no cuts: both complete bars can be given to the same child. This clarification invalidated a restriction used in `solve1.py`, `solve2.py` and `solve3.py`, and motivated the current implementations.

## 2. Current approach

### Approximate solver

`solve4.py` is the primary solution. It repeatedly looks for inexpensive local allocations in the following order:

1. Remove exact matches between a remaining bar and a remaining target. This requires no cut.
2. Match two complete bars to one child's remaining target. This also requires no cut.
3. Match one bar to two targets, including a possible dummy target representing unused chocolate. This requires one cut.
4. If none of the direct matches apply, greedily work on the largest remaining target:
   - allocate the largest complete bar smaller than the target, requiring no cut; or
   - cut the required amount from the smallest bar larger than the target, requiring one cut.

This is a local rather than global optimisation. It is not guaranteed to find the minimum number of cuts, but avoids the exponential growth of an exhaustive search and performs well on the generated test cases.

The function returns a dictionary:

{
    "cuts": cuts,
    "exact_target": exact_target,
    "target_used": adjusted_target
}

`exact_target` records whether the original request could be met. If there was insufficient chocolate, `target_used` contains the proportionally reduced allocation used by the solver.

### Exact reference solver

`solve5.py` searches the complete state space under the corrected assumptions. It uses a deque and treats allocations differently according to their cost:

- Giving away a complete piece costs no cuts, so the resulting state is placed at the front of the queue.
- Splitting a piece costs one cut, so the resulting state is placed at the back.
- A `best` dictionary records the smallest number of cuts used to reach each sorted state and prevents inferior repeated work.

This makes `solve5` a useful reference for measuring the accuracy of `solve4`. It is not the preferred general solution because the number of possible states grows exponentially with the input size.

## 3. Repository structure

TakeHomeTest/
├── main.py              Entry point and hand-written examples
├── solve4.py            Primary fast approximate solution
├── solve5.py            Exact reference solution for small cases
├── helpers.py           Shared matching and target-reduction functions
├── generate_truths.py   Random cases with known exact answers
├── analysis.py          Accuracy, timing and plotting pipeline
├── solve1.py            Retained first breadth-first attempt
├── solve2.py            Retained improved breadth-first attempt
├── solve3.py            Retained greedy solver using an old assumption
└── plots/               Generated accuracy and timing figures


## 4. File descriptions and connections

### `main.py`

This is the entry point for running the code. It imports all five solver attempts, although only `solve4` and `solve5` are enabled in the `solutions` dictionary.

It contains a set of hand-written states covering:

- cases requiring no cuts;
- insufficient chocolate;
- one child receiving multiple complete pieces from different bars;
- the example supplied with the problem;
- exact use of all available chocolate;
- repeated target values; and
- larger inputs.

`exec_timer()` runs each enabled solver repeatedly, checks that it returns a consistent result and reports mean and maximum execution times.

After the hand-written checks, `main.py` runs two broader analyses:

- `solve4` alone over larger values of `m` and `n`; and
- `solve4` against `solve5` over smaller values, where the exact solver remains practical.

### `helpers.py`

This contains the reusable operations needed by the current solvers:

- `remove_exact_matches()` removes bar/target pairs which already agree and therefore need no cuts.
- `two_sum()` finds two values which add up to one of a set of requested totals.
- `reduce_targets()` proportionally reduces requests when there is insufficient chocolate, while maintaining a minimum allocation of one unit per child. It uses the largest-remainder method to distribute units lost by rounding down.

`solve4.py` uses all three helpers. `solve5.py` only needs `reduce_targets()` because its state search handles matching directly.

### `generate_truths.py`

`gen_states()` creates random problems for which the exact minimum number of cuts is known.

It generates `n` target values, assigns every target to one of `m` non-empty groups, and constructs each starting bar as the sum of one group. The resulting problem uses all the chocolate and always has a construction requiring exactly (n - m) cuts. This is also a lower bound: starting with `m` pieces and supplying `n` positive allocations requires at least `n` pieces, while each cut increases the number of pieces by one.

The generator requires `m <= n`. This is why an analysis with `max_n = 5` cannot contain cases above `m = 5`.

### `analysis.py`

This module connects the random generator to one or more solver functions. For each `(m,n)` case it:

1. generates `n_tests` random problems with known answers;
2. records the solver output and execution time;
3. checks that the returned number of cuts is not below the known lower bound;
4. calculates accuracy, median time and mean time;
5. produces accuracy and timing plots against both `n` and `n/m`; and
6. plots the distribution of additional cuts used above the known minimum.

When given several solvers, `run_analysis()` creates separate figures for each solver and combined figures for direct comparison. Colours distinguish values of `m`, while line styles distinguish solver functions. Point markers ensure that a series containing only one valid case, such as `m = n = 5`, remains visible.

The cut-difference histogram gives more information than the percentage accuracy alone. For each trial it calculates:

```text
cuts found - known minimum cuts
```

A value of zero means that the solver found an optimal solution, so these successful trials are excluded from the histogram. The remaining positive values show how many unnecessary cuts were used when the solver did not find the minimum. The y-axis shows the percentage of all trials in each error-size bin. The bar heights therefore retain information about both the frequency and severity of non-optimal results, while omitting the usually dominant zero bin keeps the errors visible.

Each histogram displays the maximum `m`, maximum `n`, number of trials per `(m,n)` case, number and percentage of non-optimal trials, and total number of trials represented. Individual histograms are produced for each solver, together with an overlaid comparison when more than one solver is analysed. Every histogram is saved twice: a linear y-axis version gives the clearest view of the most common errors, while a logarithmic version makes rare error sizes easier to see. If every trial is optimal, the plot states that there were no non-optimal trials.

Plot filenames include the solver name, maximum `m`, maximum `n`, number of tests, measurement type and axis variant. This prevents the different figures from overwriting one another. Generated figures are saved in `plots/`.

For a fair solver-to-solver comparison, pass a fixed seed. `run_experiment()` resets the random generator for each solver, so a shared seed makes them receive the same sequence of test problems. With `seed=None`, each solver receives a different random sample.

### `solve1.py`

This is the original breadth-first search. It tries every possible split of every remaining bar and therefore explores a very large number of states. It does not track visited states, uses an inefficient list as a queue and does not robustly handle branches with no solution.

It is retained as a record of the first approach, but is not used by `main.py` because it is both incomplete and computationally impractical.

### `solve2.py`

This improves the first breadth-first search by using a `deque`, tracking visited states, restricting candidate cuts to target values and pruning branches which cannot satisfy the remaining requests.

Despite these improvements, its state space still grows exponentially. More importantly, it retains the original incorrect assumption that each child's amount must be obtained as a single piece. It is therefore retained for development history but is not used in the current comparison.

### `solve3.py`

This replaces the exponential search with a greedy allocation. Targets are processed from largest to smallest and assigned to the bar which leaves the smallest remainder. The resulting algorithm is much faster, but it still assumes that each child must receive one piece from one bar.

That assumption means it rejects valid cases such as `start = [3,3]`, `target = [6]`. It is retained to document the transition from exhaustive to approximate methods, but is no longer used.

### `solve4.py`

This is the preferred solution. It incorporates the clarified rule that children may receive multiple pieces from multiple bars, combines zero- and one-cut matching with a greedy fallback, and scales to substantially larger test cases than an exhaustive search.

### `solve5.py`

This is the exact implementation under the corrected assumptions. It is used as a small-case benchmark for `solve4`, not as the main solver, because its exhaustive state search becomes expensive as `m`, `n` and the bar sizes grow.

### `plots/`

This directory contains generated PNG figures. The plots are outputs of `analysis.py`, rather than inputs to the solution. They record accuracy, the distribution of additional cuts and median execution time for individual solvers and for direct `solve4`/`solve5` comparisons.

## 5. Running the code

The code requires Python together with NumPy and Matplotlib. From the repository directory, run:

python main.py

The hand-written examples are printed first. The analysis then runs the configured random trials, displays the figures and saves them under `plots/`.

The exact solver can become slow very quickly. The comparison in `main.py` therefore limits both `max_m` and `max_n` to 5, while the larger analysis only uses `solve4`.

## 6. Using the solvers directly

```python
from solve4 import solve4
from solve5 import solve5

start = [2,5,7]
target = [4,3,2,1]

approximate_result = solve4(start,target)
exact_result = solve5(start,target)
```

To analyse one solver:

```python
from analysis import run_analysis
from solve4 import solve4

run_analysis(
    ("solve4",solve4),
    max_n=30,
    max_m=10,
    n_tests=1000,
    seed=1
)
```

To compare the two current solvers on the same generated cases:

```python
from analysis import run_analysis
from solve4 import solve4
from solve5 import solve5

run_analysis(
    [("solve4",solve4),("solve5",solve5)],
    max_n=5,
    max_m=5,
    n_tests=10000,
    seed=1
)
```

## 7. Trade-off

The final design deliberately keeps both a practical approximation and an exact reference:

- `solve4` prioritises useful execution time and generally gets close to the minimum number of cuts.
- `solve5` guarantees the global minimum, but only remains practical for small inputs.

The generated truth cases and comparison plots make that trade-off measurable rather than relying only on a few selected examples.


## 8. Analysis findings

The generated tests measure both the accuracy and execution time of the approximate `solve4` algorithm. Each test case has a known minimum of `n - m` cuts.

For small cases up to `m = n = 5`, both `solve4` and the exact `solve5` algorithm achieved 100% accuracy across 10,000 generated tests per `(m,n)` combination. However, `solve5` became substantially slower as the problem size increased, reaching hundreds of microseconds for some cases while `solve4` remained close to a few microseconds.

The larger `solve4` analysis used up to 10 starting bars, 30 children and 1,000 tests per `(m,n)` combination. Its accuracy depended on the relationship between `m` and `n`. Accuracy was initially 100%, fell to approximately 68–80% for some intermediate cases, and generally recovered towards 96–100% as `n` approached 30.

Plotting accuracy against `n/m` shows that the loss of accuracy is grouped most strongly around `n/m = 1.5–2`. At `n/m = 1`, every group created by the test generator contains exactly one target, so the starting bars and targets can be resolved by exact matching. Just above this ratio, only a small number of bars need to supply more than one target. These cases are tightly constrained: if the exact and two-sum checks do not find the correct grouping, the greedy fallback may allocate a complete smaller bar or cut a larger bar in a way which is locally sensible but prevents the globally optimal arrangement later. The common trough across several values of `m` is consistent with this limitation. It does not prove that every error has this cause, but it identifies the regime in which the lack of look-ahead is most costly.

The cut-difference histogram complements the binary accuracy measure by showing how far the non-optimal results were from the minimum. Successful trials are excluded from the bars, while the annotation reports the total number and percentage of non-optimal trials. The size and spread of the remaining distribution therefore show both the frequency and severity of the approximation error.

The large `solve4` analysis was repeated with `seed=1` and contained 255,000 trials in total. Of these, 237,118 (92.99%) found the known minimum and 17,882 (7.01%) did not. Encouragingly, the approximation errors were heavily concentrated close to the optimum: 17,424 trials were one additional cut above the minimum. This represents 6.83% of all trials and 97.44% of the non-optimal trials. Only 452 trials (0.177% of all trials) were two cuts above the minimum, and 6 trials (0.00235%) were three cuts above it. No trial in this analysis used more than three additional cuts. Therefore, although `solve4` does not always find the global minimum, almost every failure in the tested distribution was only one cut away.

Median execution time increased smoothly with `n`, reaching approximately 100–120 microseconds at `n = 30`. The timing curves suggest non-linear growth, but remain controlled over the tested range.

These results support using `solve4` as the main solution: it sacrifices some accuracy on a recognisable region of the input space in exchange for much better scaling. `solve5` achieved 100% accuracy over the tested small cases and is designed to search for the global minimum. However, I could not empirically confirm 100% accuracy for larger `m` and `n`, because its exponential growth made a comparable number of trials impractical. The large-case plots therefore evaluate `solve4` against the known `n-m` minimum directly, rather than using `solve5` as an oracle.

### Weaknesses and possible improvements

The main weakness of `solve4` is that its fallback makes an irreversible local choice without considering how that choice affects the remaining bars and targets. The preliminary exact-match and two-sum checks avoid many unnecessary cuts, but they do not detect combinations involving three or more values. The result can also depend on which equally attractive candidate is chosen first. These limitations explain why `solve4` should be described as an approximation rather than a minimum-cut algorithm.

Possible improvements include:

- adding a bounded look-ahead before committing to a greedy allocation;
- using a beam search to retain a small number of promising states rather than only one;
- extending the direct matching stage with bounded subset-sum checks for combinations involving more than two values;
- running the greedy solver with several deterministic tie-breaking strategies and keeping the best result; and
- combining `solve4` with an exact branch-and-bound search which uses the greedy result as an initial upper bound and stops after a configurable time or state limit.

These approaches would provide intermediate trade-offs between the speed of `solve4` and the guarantee offered by `solve5`. Further evaluation should use fixed seeds for paired solver comparisons, include deliberately difficult cases around `n/m = 1.5–2`, and test adversarial inputs rather than relying only on the random generator.

Timing values are specific to the machine and Python environment used for the analysis. Accuracy results are also tied to the generated test distribution, whose target values are sampled between 1 and 20.
