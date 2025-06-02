import time
import os
import csv
from random import choices
from itertools import product
from statistics import mean
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------
# Feedback + Strategies
# ------------------------

def get_feedback(secret_code, guess):
    black = sum(s == g for s, g in zip(secret_code, guess))
    white = sum(min(secret_code.count(c), guess.count(c)) for c in set(guess)) - black
    return black, white

def filter_candidates(candidates, guess, feedback):
    black, white = feedback
    return [c for c in candidates if get_feedback(c, guess) == (black, white)]

def calculate_color_probabilities(candidates, COLORS, CODE_LENGTH):
    color_counts = {color: 0 for color in COLORS}
    for candidate in candidates:
        for color in candidate:
            color_counts[color] += 1
    total = len(candidates) * CODE_LENGTH
    return {color: color_counts[color] / total for color in COLORS}

def attempts_by_random(secret_code, all_candidates, CODE_LENGTH, MAX_ATTEMPTS):
    candidates = all_candidates.copy()
    attempts = 0
    while attempts < MAX_ATTEMPTS and candidates:
        guess = choices(candidates, k=1)[0]
        feedback = get_feedback(secret_code, guess)
        if feedback[0] == CODE_LENGTH:
            return attempts + 1
        candidates = filter_candidates(candidates, guess, feedback)
        attempts += 1
    return MAX_ATTEMPTS + 1

def attempts_by_entropy_approach(secret_code, all_candidates, COLORS, CODE_LENGTH, MAX_ATTEMPTS):
    candidates = all_candidates.copy()
    attempts = 0
    while attempts < MAX_ATTEMPTS and candidates:
        color_probs = calculate_color_probabilities(candidates, COLORS, CODE_LENGTH)
        guess = max(candidates, key=lambda c: sum(color_probs[color] for color in c))
        feedback = get_feedback(secret_code, guess)
        if feedback[0] == CODE_LENGTH:
            return attempts + 1
        candidates = filter_candidates(candidates, guess, feedback)
        attempts += 1
    return MAX_ATTEMPTS + 1

def attempts_by_knuth_algorithm(secret_code, all_candidates, CODE_LENGTH, MAX_ATTEMPTS):
    candidates = all_candidates.copy()
    attempts = 0
    while attempts < MAX_ATTEMPTS and candidates:
        guess = candidates[0]
        feedback = get_feedback(secret_code, guess)
        if feedback[0] == CODE_LENGTH:
            return attempts + 1
        candidates = filter_candidates(candidates, guess, feedback)
        attempts += 1
    return MAX_ATTEMPTS + 1

# ------------------------
# Benchmarking + Logging
# ------------------------

RESULTS_FILE = 'results.csv'

def log_to_csv(row):
    file_exists = os.path.exists(RESULTS_FILE)
    with open(RESULTS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Algorithm', 'Slots', 'NumColors', 'Runs', 'AvgAttempts', 'AvgTime'])
        writer.writerow(row)

def benchmark_algorithms(RUNS, SLOTS, COLORS):
    CODE_LENGTH = SLOTS
    MAX_ATTEMPTS = 10
    all_candidates = [''.join(p) for p in product(COLORS, repeat=SLOTS)]

    stats = { 'Random': [], 'Entropy': [], 'Knuth': [] }
    times = { 'Random': [], 'Entropy': [], 'Knuth': [] }

    for _ in range(RUNS):
        secret_code = ''.join(choices(COLORS, k=CODE_LENGTH))
        for algo, func in [
            ('Random', attempts_by_random),
            ('Entropy', attempts_by_entropy_approach),
            ('Knuth', attempts_by_knuth_algorithm)
        ]:
            start = time.time()
            attempts = func(secret_code, all_candidates, CODE_LENGTH, MAX_ATTEMPTS) if algo != 'Entropy' else func(secret_code, all_candidates, COLORS, CODE_LENGTH, MAX_ATTEMPTS)
            end = time.time()
            stats[algo].append(attempts)
            times[algo].append(end - start)

    print(f"\n📊 Configuration: SLOTS={SLOTS}, COLORS={len(COLORS)}, RUNS={RUNS}")
    print("=" * 60)
    print(f"{'Algorithm':<12}{'Avg Attempts':<15}{'Avg Time (s)':<15}")
    print("-" * 60)
    for algo in stats:
        avg_attempts = round(mean(stats[algo]), 2)
        avg_time = round(mean(times[algo]), 4)
        print(f"{algo:<12}{avg_attempts:<15}{avg_time:<15}")
        log_to_csv([algo, SLOTS, len(COLORS), RUNS, avg_attempts, avg_time])
    print("=" * 60)

# ------------------------
# Plotting
# ------------------------

def plot_results(csv_file=RESULTS_FILE):
    import pandas as pd
    sns.set(style="whitegrid")
    df = pd.read_csv(csv_file)

    # Attempts vs Algorithm
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x='Algorithm', y='AvgAttempts', ci=None)
    plt.title("Average Attempts by Algorithm")
    plt.tight_layout()
    plt.savefig("avg_attempts_per_algorithm.png")
    plt.close()

    # Time vs Algorithm
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x='Algorithm', y='AvgTime', ci=None)
    plt.title("Average Time by Algorithm")
    plt.tight_layout()
    plt.savefig("avg_time_per_algorithm.png")
    plt.close()

    # Attempts vs Slots
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df, x='Slots', y='AvgAttempts', hue='Algorithm', marker='o')
    plt.title("Avg Attempts vs Slot Count")
    plt.tight_layout()
    plt.savefig("attempts_vs_slots.png")
    plt.close()

    # Attempts vs NumColors
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df, x='NumColors', y='AvgAttempts', hue='Algorithm', marker='o')
    plt.title("Avg Attempts vs Number of Colors")
    plt.tight_layout()
    plt.savefig("attempts_vs_colors.png")
    plt.close()

    print("✅ Plots saved successfully.")

# ------------------------
# Run Benchmarks
# ------------------------

if __name__ == "__main__":
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

    # Plot at the end
    plot_results()
