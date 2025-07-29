# tools/commit_excuse.py
import random
import httpx

FALLBACK_EXCUSES = [
    "It worked on my machine... I swear.",
    "The cat walked on my keyboard. I have no idea what this commit does.",
    "This was supposed to be on another branch.",
    "It's not a bug, it's an undocumented feature.",
    "My brain had already clocked out for the weekend."
]

# The function now accepts an optional 'previous_excuse'
def get_excuse(previous_excuse: str = None ) -> str:
    """
    Tries to fetch a funny commit message, avoiding the previous one.
    If it fails, returns a fallback excuse.
    """
    try:
        headers = {"Accept": "text/plain"}
        response = httpx.get("https://whatthecommit.com/index.txt", headers=headers, timeout=3.0 )
        response.raise_for_status()
        excuse = response.text.strip()

        # If the new API excuse is the same as the last one, get another one.
        # This is a simple way to handle the rare case of an API repeat.
        if excuse == previous_excuse:
            return get_fallback_excuse(previous_excuse)
        
        return excuse
    except (httpx.RequestError, httpx.HTTPStatusError ):
        return get_fallback_excuse(previous_excuse)

def get_fallback_excuse(previous_excuse: str = None) -> str:
    """Gets a random excuse from the fallback list, avoiding the previous one."""
    if len(FALLBACK_EXCUSES) <= 1:
        return FALLBACK_EXCUSES[0]
        
    possible_excuses = [e for e in FALLBACK_EXCUSES if e != previous_excuse]
    return random.choice(possible_excuses)
