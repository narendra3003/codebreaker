from random import choices
from random_solver import random_solver
from knuth_solver import knuth_solver
from solvers.greedy_solver import greedy_solver
from solver_utils import COLORS, CODE_LENGTH

def generate_secret_code():
    return choices(COLORS, k=4)
    # return choices(COLORS, k=CODE_LENGTH)

def main():
    secret_code = generate_secret_code()
    print(f"🔐 Secret Code Generated (Hidden): {secret_code}")

    print("\n🎲 Random Solver")
    print("Attempts:", random_solver(secret_code))

    print("\n📐 Knuth Solver")
    print("Attempts:", knuth_solver(secret_code))

    print("\n🧠 Greedy Solver")
    print("Attempts:", greedy_solver(secret_code))

if __name__ == "__main__":
    main()
