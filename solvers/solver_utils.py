from itertools import product

COLORS = ['R', 'G', 'B', 'Y', 'O', 'P']
SLOTS = 4
CODE_LENGTH = 4

# Generate all candidates
all_candidates = [''.join(p) for p in product(COLORS, repeat=SLOTS)]

def get_feedback(secret_code, guess):
    black = sum(s == g for s, g in zip(secret_code, guess))
    white = sum(min(secret_code.count(c), guess.count(c)) for c in set(guess)) - black
    return black, white

def filter_candidates(candidates, guess, feedback):
    black, white = feedback
    return [c for c in candidates if get_feedback(c, guess) == (black, white)]

def calculate_color_probabilities(candidates):
    color_counts = {color: 0 for color in COLORS}
    for candidate in candidates:
        for color in candidate:
            color_counts[color] += 1
    total = len(candidates) * CODE_LENGTH
    return {color: round(color_counts[color] / total, 2)*4 for color in COLORS}
