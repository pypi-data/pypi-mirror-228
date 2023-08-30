# authorization.py

API_KEY = "kangtools"

USER_PROVIDED_KEY = None

def set_api_key(key):
    global USER_PROVIDED_KEY
    USER_PROVIDED_KEY = key

def authorize():
    if USER_PROVIDED_KEY != API_KEY:
        raise PermissionError("Invalid API key! if you want to use this, please contact xiaowen kang kangxiaowen@gamil.com")

def authorization_decorator(func):
    def wrapper(*args, **kwargs):
        authorize()
        return func(*args, **kwargs)
    return wrapper
