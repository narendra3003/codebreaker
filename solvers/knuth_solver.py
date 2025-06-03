from solver_utils import get_feedback, filter_candidates, all_candidates, CODE_LENGTH, COLORS
from collections import defaultdict

def score_guess(guess, candidates):
    """Count the worst-case number of remaining possibilities for each feedback."""
    feedback_counts = defaultdict(int)
    for code in candidates:
        feedback = get_feedback(code, guess)
        feedback_counts[feedback] += 1
    return max(feedback_counts.values())

def select_minimax_guesses(all_codes, candidates):
    """Return all guesses with the best (minimal worst-case) score."""
    scores = {}
    for guess in all_codes:
        scores[guess] = score_guess(guess, candidates)
    min_score = min(scores.values())
    return [g for g, score in scores.items() if score == min_score]

def get_next_guess(minimax_guesses, candidates, all_codes):
    """Prefer a minimax guess that's still a candidate, if possible."""
    for guess in minimax_guesses:
        if guess in candidates:
            return guess
    for guess in minimax_guesses:
        if guess in all_codes:
            return guess
    return minimax_guesses[0]

def knuth_solver(secret_code, all_codes=None, max_attempts=10):
    if all_codes is None:
        from itertools import product
        all_codes = [''.join(p) for p in product(COLORS, repeat=CODE_LENGTH)]

    candidates = all_codes.copy()
    guess = 'RRGG'[:CODE_LENGTH]  # Initial guess; adjust for other lengths if needed
    attempts = 1

    while attempts <= max_attempts:
        feedback = get_feedback(secret_code, guess)
        if feedback[0] == CODE_LENGTH:
            print("Code cracked!")
            return attempts

        candidates = filter_candidates(candidates, guess, feedback)
        minimax_guesses = select_minimax_guesses(all_codes, candidates)
        guess = get_next_guess(minimax_guesses, candidates, all_codes)
        attempts += 1

    print(f"Failed to solve the code {secret_code} within {max_attempts} attempts.")
    return max_attempts + 1
