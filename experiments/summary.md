# Mastermind Solver Benchmark Summary

This document summarizes the performance benchmarks of various solver strategies implemented in the **CodeBreaker** project. Each strategy was tested across different game configurations to measure both average number of attempts and runtime efficiency.

## 🔬 Experimental Setup

- **Solvers Tested**: Random, Greedy, Fixed Start, Knuth
- **Variables**:
  - Number of slots: 3, 4, 5
  - Number of colors: 4, 5, 6
  - Runs per setting: 10, 50, 100
- **Metrics Collected**:
  - Average Attempts to Solve
  - Average Time (seconds)

---

## 📈 Key Insights

- **Random Strategy**:
  - Performs surprisingly well at smaller configurations (3–4 slots, 4–5 colors).
  - Scales well in runtime even for larger configs.
  - Remains competitive in average attempts due to uniform randomness over limited space.

- **Greedy Strategy**:
  - Consistently slower in solving than Random and Knuth.
  - Suffers in both average attempts and runtime as slots/colors increase.

- **Fixed Start**:
  - Offers stable but not optimal results; generally better than Greedy but worse than Knuth.
  - Good fallback strategy with predictable performance.

- **Knuth's Algorithm**:
  - **Best in terms of attempts** across nearly all configurations.
  - **Scales poorly** in runtime—becomes extremely slow at higher slot/color counts.
  - Still usable up to (4, 6), but beyond that becomes impractical.

---

## 📊 Performance Trends

| Algorithm     | Strengths                      | Weaknesses                           |
|---------------|-------------------------------|--------------------------------------|
| Random        | Fast, decent attempts          | Not optimal, still stochastic        |
| Greedy        | Simple                         | High attempts, not scalable          |
| Fixed Start   | Stable                         | Never best in class                  |
| Knuth         | Best in logic, fewest attempts | Slow at large scales                 |

---

## 📁 Raw Data

Full benchmark data is available in [`results.csv`](./results.csv).

---

## 📌 Notes

- Benchmarking was done using Python implementations.
- For real-time applications or large-scale games, Knuth may need optimization or replacement.
- This summary supports choosing a solver based on trade-offs between speed and accuracy.

