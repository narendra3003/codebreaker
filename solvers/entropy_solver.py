from solvers.solver_utils import get_feedback, filter_candidates, calculate_color_probabilities, all_candidates, CODE_LENGTH

def entropy_solver(secret_code, max_attempts=10):
    candidates = all_candidates.copy()
    attempts = 0
    while attempts < max_attempts and candidates:
        color_probs = calculate_color_probabilities(candidates)
        guess = max(candidates, key=lambda c: sum(color_probs[color] for color in c))
        feedback = get_feedback(secret_code, guess)
        if feedback[0] == CODE_LENGTH:
            return attempts + 1
        candidates = filter_candidates(candidates, guess, feedback)
        attempts += 1
    print(f"Failed to solve the code {secret_code} within {max_attempts} attempts.")
    return max_attempts + 1

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