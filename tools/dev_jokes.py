# tools/dev_jokes.py
import random
import httpx
import os

# --- The reliable, offline fallback list ---
FALLBACK_JOKES = [
    "Why do Java developers wear glasses? Because they don't C#!",
    "What's a programmer's favorite hangout place? Foo Bar.",
    "Why did the developer go broke? Because he used up all his cache."
]

def get_joke( ) -> str:
    """
    Tries to fetch a joke from an API. If it fails, returns a joke
    from the reliable fallback list.
    """
    try:
        # This is a free, public joke API. No key needed.
        # For an LLM, you would call its specific endpoint here.
        response = httpx.get(
            "https://official-joke-api.appspot.com/jokes/programming/random",
            timeout=3.0 # Set a timeout to prevent long waits
         )
        response.raise_for_status() # Raise an exception for bad responses (4xx or 5xx)
        
        data = response.json()[0]
        joke = f"{data['setup']} {data['punchline']}"
        return joke

    except (httpx.RequestError, httpx.HTTPStatusError, KeyError, IndexError ) as e:
        # If anything goes wrong with the network request or data parsing...
        print(f"[API Error: {e}. Using fallback.]") # Optional: for debugging
        # ...just return a joke from our safe, offline list.
        return random.choice(FALLBACK_JOKES)

