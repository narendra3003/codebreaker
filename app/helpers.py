from itertools import product
from random import choice

def generate_all_candidates(colors, slots):
    return list(product(colors, repeat=slots))

def generate_secret_code(colors, length):
    return [choice(colors) for _ in range(length)]

def get_feedback(secret, guess):
    black = sum(s == g for s, g in zip(secret, guess))
    whites = sum(min(secret.count(c), guess.count(c)) for c in set(guess)) - black
    return black, whites

def filter_candidates(candidates, guess, feedback):
    black, whites = feedback
    return [c for c in candidates if get_feedback(c, guess) == (black, whites)]

def calculate_color_probabilities_by_position(candidates, slots, colors):
    color_probability_by_position = {i: {color: 0 for color in colors} for i in range(slots)}
    for candidate in candidates:
        for i, color in enumerate(candidate):
            color_probability_by_position[i][color] += 1
    total = len(candidates)
    if total > 0:
        for i in range(slots):
            for color in colors:
                color_probability_by_position[i][color] /= total
    return color_probability_by_position
