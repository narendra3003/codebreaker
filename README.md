# 🎰 CodeBreaker: CodeBreaker Game with AI Solvers

A Python-based implementation of the classic **CodeBreaker** game — with a GUI, probability-based helper hints, and solver strategies.
---

## 🎮 Features

- 🎨 **Interactive GUI** with color pickers and feedback system
- 🎯 **Custom difficulty**: Adjustable code length and color pool
- 🔍 **Smart hints**: Probability-based suggestions after each guess
- 🤖 **Solver AI bots**:
  - **Random Guesser**
  - **Knuth’s Algorithm**
  - **Greedy Solver**
- 📊 **Benchmarking engine**: Run simulations for different configurations, track average guesses & runtimes

---

## 🧩 Gameplay

Try to guess the hidden color sequence within limited attempts. After each guess:
- ⚫ Black peg = correct color in the correct position
- ⚪ Gray peg = correct color but wrong position
- ⬜ Light gray = incorrect color

---

## ⚙️ Configuration

You can customize:
- Number of colors (`4–10`)
- Code length (`4–6`)
- Get Probability hints

Modify values in `app/settings.py` or pass as parameters in solver/benchmark scripts.

---

## 🚀 Download Executable

You can download the latest `.exe` version of the CodeBreaker game here:

👉 [CodeBreaker v1.0 Release](https://github.com/narendra3003/codebreaker/releases/latest)

No installation required — just extract and run `codebreaker.exe`.

---

## 📁 Project Structure

```bash
codebreaker/
├── app/              # GUI and helper logic
│   ├── __init__.py
│   ├── gui.py
│   ├── helpers.py
│   └── settings.py
│
├── solvers/          # AI solvers
│   ├── random_solver.py
│   ├── knuth_solver.py
│   ├── greedy_solver.py
│   └── solver_utils.py
│
├── experiments/      # Benchmarking experiment
│   ├── benchmark_runner.py
│   └── results.csv
│
├── assets/           # Images of plots
|
|
├── README.md
├── LICENSE
├── .gitignore
└── requirements.txt
````

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Game

```bash
python app/gui.py
```

### 3. Run Benchmarks
Just click on ▷ button in sidebar

---

## 📊 Sample Benchmark Output

📊 Configuration: SLOTS=5, COLORS=5, RUNS=50
============================================================
Algorithm   Avg Attempts   Avg Time (s)   
------------------------------------------------------------
Random      4.64           0.0088         
Greedy      5.38           0.0117         
fixed_start 5.24           0.0081         
Knuth       4.46           2.8326         
============================================================

---

## 🛠️ Built With

* Python 🐍
* Tkinter 🎨
* itertools, random, time, statistics
* Solver logic inspired by Donald Knuth’s 5-guess algorithm

---

## 📌 Ideas for Future Work

* Add leaderboard or score tracking
* CLI version for solvers
* Export game history
* Web version using Flask or PyScript

---

## 📄 License

This project is licensed under the MIT License.

---

## 🤝 Connect

Feel free to fork, use, or modify — and drop a ⭐ if you liked it!
