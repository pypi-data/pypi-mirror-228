API_KEY = "kangtools"

def authorize(key):
    if key != API_KEY:
        raise ImportError("Invalid API key. Please contact the package author for a valid key.")

