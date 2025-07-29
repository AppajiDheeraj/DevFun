# tools/code_roast.py
import random

CODE_ROASTS = [
    "Your code is so bad, Git refused to track it.",
    "If your code was a person, it would still be living in its parent's basement.",
    "I'm not saying your code is spaghetti, but the Italians are impressed.",
    "Your code is the reason 'technical debt' was invented.",
    "I've seen better error handling in a 1980s VCR."
]

def get_roast() -> str:
    """Returns a random code roast."""
    return random.choice(CODE_ROASTS)