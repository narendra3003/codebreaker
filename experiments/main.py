from benchmark_runner import benchmark_algorithms
color_sets = [
    ['R', 'G', 'B', 'Y', 'O', 'P'],
    ['R', 'G', 'B', 'Y'],
    ['R', 'G', 'B', 'Y', 'O', 'P', 'C'],
]

slot_configs = [3, 4, 5]
run_counts = [10, 50, 100]

for COLORS in color_sets:
    for SLOTS in slot_configs:
        for RUNS in run_counts:
            benchmark_algorithms(RUNS, SLOTS, COLORS)
