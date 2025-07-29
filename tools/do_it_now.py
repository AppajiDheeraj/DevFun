# tools/do_it_now.py
import random

DO_IT_NOW_MESSAGES = [
    "Stop scrolling. Start building. NOW.",
    "The best time to start was yesterday. The second best time is now.",
    "Code something amazing before you forget the idea.",
    "Don't just think about it. Do it!",
    "Your future self will thank you for the code you write today."
]

def get_motivation() -> str:
    """Returns a random motivational message."""
    return random.choice(DO_IT_NOW_MESSAGES)
