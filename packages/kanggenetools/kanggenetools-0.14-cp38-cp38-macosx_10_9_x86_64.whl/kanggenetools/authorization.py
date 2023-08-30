# authorization.py

API_KEY = "kangtools"

def authorize(provided_key):
    if provided_key != API_KEY:
        raise PermissionError("Invalid API key")
