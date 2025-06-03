from random import choices
from solver_utils import get_feedback, filter_candidates, all_candidates, CODE_LENGTH

def random_solver(secret_code, max_attempts=10):
    candidates = all_candidates.copy()
    attempts = 0
    while attempts < max_attempts and candidates:
        guess = choices(candidates, k=1)[0]
        feedback = get_feedback(secret_code, guess)
        if feedback[0] == CODE_LENGTH:
            return attempts + 1
        candidates = filter_candidates(candidates, guess, feedback)
        attempts += 1
    print(f"Failed to solve the code {secret_code} within {max_attempts} attempts.")
    return max_attempts + 1  # Failed

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

def attempts_by_fixed_then_random(secret_code, all_candidates, CODE_LENGTH, MAX_ATTEMPTS, initial_guess='RRGG'):
    candidates = all_candidates.copy()
    attempts = 0
    feedback = get_feedback(secret_code, initial_guess)
    attempts += 1
    if feedback[0] == CODE_LENGTH:
        return attempts
    candidates = filter_candidates(candidates, initial_guess, feedback)
    
    while attempts < MAX_ATTEMPTS and candidates:
        guess = choices(candidates, k=1)[0]
        feedback = get_feedback(secret_code, guess)
        if feedback[0] == CODE_LENGTH:
            return attempts + 1
        candidates = filter_candidates(candidates, guess, feedback)
        attempts += 1
        
    return MAX_ATTEMPTS + 1